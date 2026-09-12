from __future__ import annotations

from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Literal
from uuid import uuid4
import hashlib
import json

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RequestType(StrEnum):
    INITIAL_COLLECTION = "initial_collection"
    CLARIFICATION = "clarification"
    RENEWAL_CHANGES = "renewal_changes"


class RequestStatus(StrEnum):
    DRAFT = "draft"
    PREPARING = "preparing"
    AWAITING_APPROVAL = "awaiting_approval"
    QUEUED = "queued"
    COLLECTING = "collecting"
    WAITING = "waiting"
    NEEDS_REVIEW = "needs_review"
    READY_FOR_REVIEW = "ready_for_review"
    PAUSED = "paused"
    COMPLETED = "completed"
    CLOSED_PARTIAL = "closed_partial"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    FAILED = "failed"


class UiGroup(StrEnum):
    NEEDS_YOU = "needs_you"
    RUNNING = "running"
    DONE = "done"


class Contact(BaseModel):
    id: str
    name: str
    organization: str
    email: EmailStr
    role: str
    authorized: bool = True
    suppressed: bool = False


class Question(BaseModel):
    id: str
    label: str
    required: bool = True
    dataType: str = "string"
    unitsHint: str | None = None
    periodHint: str | None = None
    evidenceRule: str = "reported"


class Template(BaseModel):
    id: RequestType
    name: str
    description: str
    questions: list[Question]


class PlanRespondent(BaseModel):
    contactId: str
    name: str
    organization: str
    email: EmailStr


class PlanMethod(BaseModel):
    channel: Literal["email"] = "email"
    reminderCount: int = Field(default=1, ge=0, le=2)
    reminderAfterHours: int = Field(default=48, ge=24)


class PlanLimits(BaseModel):
    deadline: datetime
    maxTouches: int = Field(default=3, ge=1, le=3)
    forbiddenChannels: list[str] = Field(default_factory=list)


class RequestPlan(BaseModel):
    version: int = 1
    objective: str
    requestType: RequestType
    respondent: PlanRespondent | None
    questions: list[Question]
    alreadyAvailable: list[str] = Field(default_factory=list)
    method: PlanMethod = Field(default_factory=PlanMethod)
    limits: PlanLimits
    deliverable: str = "Email a source-linked summary to the requester."
    blockingClarifications: list[str] = Field(default_factory=list)
    planHash: str


class Event(BaseModel):
    sequence: int
    type: str
    message: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Answer(BaseModel):
    questionId: str
    question: str
    rawValue: str | None = None
    normalizedValue: str | None = None
    status: Literal["open", "answered", "unavailable", "conflicting", "waived"]
    evidenceStatus: Literal["reported", "document_supported", "human_confirmed"] | None = None
    source: str | None = None


class RequestResult(BaseModel):
    version: int = 1
    status: Literal["complete", "partial"]
    summary: str
    answers: list[Answer]
    unresolvedItems: list[str] = Field(default_factory=list)
    generatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InformationRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(default_factory=lambda: f"req_{uuid4().hex[:10]}")
    instruction: str
    status: RequestStatus = RequestStatus.PREPARING
    uiGroup: UiGroup = UiGroup.RUNNING
    ownerEmail: EmailStr = "operator@example.com"
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1
    activePlan: RequestPlan | None = None
    result: RequestResult | None = None
    allowedActions: list[str] = Field(default_factory=list)
    events: list[Event] = Field(default_factory=list)


class RequestCreate(BaseModel):
    instruction: str = Field(min_length=8)
    ownerEmail: EmailStr = "operator@example.com"


class ApprovalCreate(BaseModel):
    planVersion: int
    planHash: str


class ControlCommand(BaseModel):
    action: Literal["pause", "resume", "cancel"]


class ReviewCreate(BaseModel):
    action: Literal["accept", "close_partial"]
    resultVersion: int
    reason: str | None = None


class RequestListResponse(BaseModel):
    needsYou: list[InformationRequest]
    running: list[InformationRequest]
    done: list[InformationRequest]


def default_deadline(days: int = 5) -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=days)


def compute_plan_hash(plan_payload: dict) -> str:
    payload = dict(plan_payload)
    payload.pop("planHash", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def compute_ui_group(status: RequestStatus | str) -> UiGroup:
    value = RequestStatus(status)
    if value in {
        RequestStatus.DRAFT,
        RequestStatus.AWAITING_APPROVAL,
        RequestStatus.NEEDS_REVIEW,
        RequestStatus.READY_FOR_REVIEW,
        RequestStatus.PAUSED,
    }:
        return UiGroup.NEEDS_YOU
    if value in {RequestStatus.PREPARING, RequestStatus.QUEUED, RequestStatus.COLLECTING, RequestStatus.WAITING}:
        return UiGroup.RUNNING
    return UiGroup.DONE
