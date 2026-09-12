from __future__ import annotations

from datetime import datetime, timezone

from app.domain.models import (
    PlanLimits,
    PlanMethod,
    PlanRespondent,
    RequestPlan,
    RequestType,
    compute_plan_hash,
    default_deadline,
)
from app.domain.templates import TEMPLATES
from app.persistence.in_memory import InMemoryStore


def compile_plan(instruction: str, store: InMemoryStore) -> RequestPlan:
    """Deterministic M1 intent compiler.

    This is intentionally conservative and fake-provider backed. A real model adapter can
    replace candidate extraction later, but contact resolution and policy checks should
    remain deterministic application code.
    """

    lowered = instruction.lower()
    request_type = classify_request_type(lowered)
    template = TEMPLATES[request_type]
    blocking: list[str] = []

    contact = resolve_contact(lowered, store)
    if contact is None:
        blocking.append("Select one approved respondent from the contact directory before any outbound action.")
        respondent = None
    elif contact.suppressed or not contact.authorized:
        blocking.append(f"{contact.name} is not currently authorized for automated contact.")
        respondent = None
    else:
        respondent = PlanRespondent(
            contactId=contact.id,
            name=contact.name,
            organization=contact.organization,
            email=contact.email,
        )

    forbidden = []
    if "don't call" in lowered or "do not call" in lowered or "no calls" in lowered or "no call" in lowered:
        forbidden.extend(["voice", "phone"])
    if "whatsapp" in lowered and "don't whatsapp" not in lowered:
        blocking.append("WhatsApp is not enabled in the pilot. Use email or narrow the instruction.")

    already_available = []
    if "last year" in lowered or "prior" in lowered or "existing" in lowered:
        already_available.append("Prior-period information mentioned by operator; source must be attached before live execution.")

    objective = build_objective(request_type, instruction)
    reminder_count = 0 if "no reminder" in lowered else 1

    payload = {
        "version": 1,
        "objective": objective,
        "requestType": request_type.value,
        "respondent": respondent.model_dump(mode="json") if respondent else None,
        "questions": [q.model_dump(mode="json") for q in template.questions],
        "alreadyAvailable": already_available,
        "method": PlanMethod(reminderCount=reminder_count).model_dump(mode="json"),
        "limits": PlanLimits(deadline=default_deadline(), maxTouches=1 + reminder_count, forbiddenChannels=forbidden).model_dump(mode="json"),
        "deliverable": "Email the requester a source-linked summary with unanswered items and evidence notes.",
        "blockingClarifications": blocking,
    }
    payload["planHash"] = compute_plan_hash(payload)
    return RequestPlan.model_validate(payload)


def classify_request_type(lowered_instruction: str) -> RequestType:
    if any(word in lowered_instruction for word in ["renewal", "renew", "changed", "changes", "no change"]):
        return RequestType.RENEWAL_CHANGES
    if any(word in lowered_instruction for word in ["clarify", "clarification", "missing", "inconsistent", "gap", "figures"]):
        return RequestType.CLARIFICATION
    return RequestType.INITIAL_COLLECTION


def resolve_contact(lowered_instruction: str, store: InMemoryStore):
    contacts = store.list_contacts()

    explicit_matches = [contact for contact in contacts if contact.name.lower() in lowered_instruction or contact.email.lower() in lowered_instruction]
    if len(explicit_matches) == 1:
        return explicit_matches[0]
    if len(explicit_matches) > 1:
        return None

    if "finance" in lowered_instruction:
        return store.get_contact("contact_finance")
    if "operations" in lowered_instruction or "ops" in lowered_instruction:
        return store.get_contact("contact_ops")
    if "broker" in lowered_instruction:
        return store.get_contact("contact_broker")

    return None


def build_objective(request_type: RequestType, instruction: str) -> str:
    prefix = {
        RequestType.INITIAL_COLLECTION: "Collect initial information",
        RequestType.CLARIFICATION: "Resolve missing or inconsistent information",
        RequestType.RENEWAL_CHANGES: "Confirm renewal changes without assuming prior facts remain current",
    }[request_type]
    cleaned = " ".join(instruction.split())
    return f"{prefix}: {cleaned[:180]}"
