from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status

from app.domain.models import (
    ApprovalCreate,
    Contact,
    ControlCommand,
    InformationRequest,
    RequestCreate,
    RequestListResponse,
    RequestPlan,
    RequestResult,
    RequestStatus,
    ReviewCreate,
    Template,
)
from app.domain.templates import TEMPLATES
from app.persistence.in_memory import InMemoryStore
from app.services.planning import compile_plan
from app.services.results import build_synthetic_result

router = APIRouter(prefix="/v1")


def store_from(request: Request) -> InMemoryStore:
    return request.app.state.store


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "m1-dry-run"}


@router.get("/contacts", response_model=list[Contact])
def list_contacts(request: Request) -> list[Contact]:
    return store_from(request).list_contacts()


@router.get("/templates", response_model=list[Template])
def list_templates() -> list[Template]:
    return list(TEMPLATES.values())


@router.post("/requests", response_model=InformationRequest, status_code=status.HTTP_201_CREATED)
def create_request(payload: RequestCreate, request: Request) -> InformationRequest:
    store = store_from(request)
    info_request = InformationRequest(instruction=payload.instruction, ownerEmail=payload.ownerEmail)
    store.add_event(info_request, "request.created", "Instruction saved. Preparing a bounded plan.")

    plan = compile_plan(payload.instruction, store)
    info_request.activePlan = plan
    if plan.blockingClarifications:
        info_request.status = RequestStatus.NEEDS_REVIEW
        store.add_event(info_request, "plan.blocked", "Plan requires clarification before approval.")
    else:
        info_request.status = RequestStatus.AWAITING_APPROVAL
        store.add_event(info_request, "plan.ready", "Plan preview is ready. No outbound action has occurred.")
    return store.add_request(info_request)


@router.get("/requests", response_model=RequestListResponse)
def list_requests(request: Request) -> RequestListResponse:
    items = store_from(request).list_requests()
    return RequestListResponse(
        needsYou=[item for item in items if item.uiGroup == "needs_you"],
        running=[item for item in items if item.uiGroup == "running"],
        done=[item for item in items if item.uiGroup == "done"],
    )


@router.get("/requests/{request_id}", response_model=InformationRequest)
def get_request(request_id: str, request: Request) -> InformationRequest:
    return require_request(request_id, store_from(request))


@router.get("/requests/{request_id}/plan", response_model=RequestPlan)
def get_plan(request_id: str, request: Request) -> RequestPlan:
    info_request = require_request(request_id, store_from(request))
    if info_request.activePlan is None:
        raise HTTPException(status_code=404, detail="No plan exists for this request")
    return info_request.activePlan


@router.post("/requests/{request_id}/approvals", response_model=InformationRequest)
def approve_plan(request_id: str, payload: ApprovalCreate, request: Request) -> InformationRequest:
    store = store_from(request)
    info_request = require_request(request_id, store)
    if info_request.status != RequestStatus.AWAITING_APPROVAL:
        raise HTTPException(status_code=409, detail=f"Request is {info_request.status}; it is not awaiting approval")
    if info_request.activePlan is None:
        raise HTTPException(status_code=409, detail="Request has no active plan")
    if info_request.activePlan.version != payload.planVersion or info_request.activePlan.planHash != payload.planHash:
        raise HTTPException(status_code=409, detail="Plan version/hash is stale. Fetch the current plan before approving.")

    info_request.status = RequestStatus.READY_FOR_REVIEW
    info_request.result = build_synthetic_result(info_request.activePlan)
    store.add_event(info_request, "plan.approved", "Exact plan approved. M1 fake adapter produced a synthetic result; no email was sent.")
    store.add_event(info_request, "result.ready", "Dry-run result is ready for review.")
    return store.save_request(info_request)


@router.post("/requests/{request_id}/control", response_model=InformationRequest)
def control_request(request_id: str, payload: ControlCommand, request: Request) -> InformationRequest:
    store = store_from(request)
    info_request = require_request(request_id, store)

    if payload.action == "cancel":
        if info_request.status in terminal_statuses():
            raise HTTPException(status_code=409, detail="Request is already terminal")
        info_request.status = RequestStatus.CANCELLED
        store.add_event(info_request, "request.cancelled", "Request cancelled. No further outbound work is allowed.")
    elif payload.action == "pause":
        if info_request.status not in {RequestStatus.PREPARING, RequestStatus.QUEUED, RequestStatus.COLLECTING, RequestStatus.WAITING}:
            raise HTTPException(status_code=409, detail="Only running requests can be paused")
        info_request.status = RequestStatus.PAUSED
        store.add_event(info_request, "request.paused", "Request paused. Incoming evidence would still be stored in live mode.")
    elif payload.action == "resume":
        if info_request.status != RequestStatus.PAUSED:
            raise HTTPException(status_code=409, detail="Only paused requests can be resumed")
        info_request.status = RequestStatus.AWAITING_APPROVAL if info_request.activePlan else RequestStatus.PREPARING
        store.add_event(info_request, "request.resumed", "Request resumed after a fresh state check.")

    return store.save_request(info_request)


@router.get("/requests/{request_id}/events")
def list_events(request_id: str, request: Request):
    info_request = require_request(request_id, store_from(request))
    return {"events": info_request.events}


@router.get("/requests/{request_id}/result", response_model=RequestResult)
def get_result(request_id: str, request: Request) -> RequestResult:
    info_request = require_request(request_id, store_from(request))
    if info_request.result is None:
        raise HTTPException(status_code=404, detail="No result exists for this request")
    return info_request.result


@router.post("/requests/{request_id}/reviews", response_model=InformationRequest)
def review_result(request_id: str, payload: ReviewCreate, request: Request) -> InformationRequest:
    store = store_from(request)
    info_request = require_request(request_id, store)
    if info_request.status != RequestStatus.READY_FOR_REVIEW or info_request.result is None:
        raise HTTPException(status_code=409, detail="Request is not ready for review")
    if info_request.result.version != payload.resultVersion:
        raise HTTPException(status_code=409, detail="Result version is stale")
    if payload.action == "accept":
        if info_request.result.status != "complete":
            raise HTTPException(status_code=409, detail="Partial result cannot be accepted as complete; close partial or resume collection")
        info_request.status = RequestStatus.COMPLETED
        store.add_event(info_request, "result.accepted", "Result accepted as complete.")
    else:
        info_request.status = RequestStatus.CLOSED_PARTIAL
        store.add_event(info_request, "result.closed_partial", payload.reason or "Result closed with documented gaps.")
    return store.save_request(info_request)


def require_request(request_id: str, store: InMemoryStore) -> InformationRequest:
    info_request = store.get_request(request_id)
    if info_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return info_request


def terminal_statuses() -> set[RequestStatus]:
    return {
        RequestStatus.COMPLETED,
        RequestStatus.CLOSED_PARTIAL,
        RequestStatus.CANCELLED,
        RequestStatus.EXPIRED,
        RequestStatus.FAILED,
    }
