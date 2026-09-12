from __future__ import annotations

from datetime import datetime, timezone

from app.domain.models import Contact, Event, InformationRequest, RequestStatus, compute_ui_group


class InMemoryStore:
    """Pilot-only storage. Replace with PostgreSQL repositories in M2."""

    def __init__(self) -> None:
        self.requests: dict[str, InformationRequest] = {}
        self.contacts: dict[str, Contact] = {
            "contact_finance": Contact(
                id="contact_finance",
                name="Riya Shah",
                organization="Acme Components Pvt Ltd",
                email="riya.shah@example.com",
                role="Finance contact",
            ),
            "contact_ops": Contact(
                id="contact_ops",
                name="Arjun Mehta",
                organization="Acme Components Pvt Ltd",
                email="arjun.mehta@example.com",
                role="Operations contact",
            ),
            "contact_broker": Contact(
                id="contact_broker",
                name="Nisha Rao",
                organization="Broker Partner LLP",
                email="nisha.rao@example.com",
                role="Broker contact",
            ),
        }

    def list_contacts(self) -> list[Contact]:
        return list(self.contacts.values())

    def get_contact(self, contact_id: str) -> Contact | None:
        return self.contacts.get(contact_id)

    def add_request(self, request: InformationRequest) -> InformationRequest:
        self.requests[request.id] = self._refresh(request)
        return self.requests[request.id]

    def get_request(self, request_id: str) -> InformationRequest | None:
        request = self.requests.get(request_id)
        if request is None:
            return None
        return self._refresh(request)

    def save_request(self, request: InformationRequest) -> InformationRequest:
        request.version += 1
        request.updatedAt = datetime.now(timezone.utc)
        self.requests[request.id] = self._refresh(request)
        return self.requests[request.id]

    def list_requests(self) -> list[InformationRequest]:
        return [self._refresh(request) for request in sorted(self.requests.values(), key=lambda item: item.createdAt, reverse=True)]

    def add_event(self, request: InformationRequest, event_type: str, message: str) -> None:
        request.events.append(Event(sequence=len(request.events) + 1, type=event_type, message=message))

    def _refresh(self, request: InformationRequest) -> InformationRequest:
        request.uiGroup = compute_ui_group(request.status)
        request.allowedActions = allowed_actions(RequestStatus(request.status))
        return request


def allowed_actions(status: RequestStatus) -> list[str]:
    match status:
        case RequestStatus.AWAITING_APPROVAL:
            return ["approve", "amend", "cancel"]
        case RequestStatus.NEEDS_REVIEW:
            return ["amend", "cancel"]
        case RequestStatus.READY_FOR_REVIEW:
            return ["accept", "close_partial", "resume_collection"]
        case RequestStatus.PAUSED:
            return ["resume", "cancel"]
        case RequestStatus.PREPARING | RequestStatus.QUEUED | RequestStatus.COLLECTING | RequestStatus.WAITING:
            return ["pause", "cancel"]
        case _:
            return []
