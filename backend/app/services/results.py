from __future__ import annotations

from app.domain.models import Answer, RequestPlan, RequestResult


def build_synthetic_result(plan: RequestPlan) -> RequestResult:
    """Create a deterministic dry-run result after approval.

    M1 proves lifecycle and UI. M2 replaces this with email send/receive,
    extraction, reconciliation, and report delivery.
    """

    answers: list[Answer] = []
    unresolved: list[str] = []

    for index, question in enumerate(plan.questions):
        if index < 2:
            answers.append(
                Answer(
                    questionId=question.id,
                    question=question.label,
                    rawValue=mock_value(question.id),
                    normalizedValue=None,
                    status="answered",
                    evidenceStatus="reported",
                    source=f"Synthetic reply from {plan.respondent.name if plan.respondent else 'approved respondent'}; no real email sent.",
                )
            )
        else:
            answers.append(
                Answer(
                    questionId=question.id,
                    question=question.label,
                    rawValue=None,
                    status="open",
                    evidenceStatus=None,
                    source=None,
                )
            )
            unresolved.append(question.label)

    status = "complete" if not unresolved else "partial"
    summary = (
        "Dry-run result prepared from a synthetic reply. "
        "It demonstrates source-linked reporting and unresolved-item handling; it is not evidence from a real respondent."
    )
    return RequestResult(status=status, summary=summary, answers=answers, unresolvedItems=unresolved)


def mock_value(question_id: str) -> str:
    if "turnover" in question_id or "figures" in question_id:
        return "INR 12.4 crore for FY 2025-26 (reported; synthetic)"
    if "period" in question_id:
        return "Financial year basis ending 31 March (reported; synthetic)"
    if "activity" in question_id:
        return "No material activity change reported (synthetic)"
    return "Respondent supplied a concise answer (synthetic)"
