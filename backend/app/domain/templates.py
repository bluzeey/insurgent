from .models import Question, RequestType, Template


TEMPLATES: dict[RequestType, Template] = {
    RequestType.INITIAL_COLLECTION: Template(
        id=RequestType.INITIAL_COLLECTION,
        name="Initial collection",
        description="Collect an expert-approved starter checklist for a new information request.",
        questions=[
            Question(id="business_activity", label="Confirm current business activity and any material changes.", evidenceRule="reported"),
            Question(id="turnover_current", label="Provide current year turnover with reporting period and currency.", dataType="number", unitsHint="currency", periodHint="current reporting period", evidenceRule="reported"),
            Question(id="locations", label="Confirm insured locations or operating sites relevant to the request.", evidenceRule="reported"),
        ],
    ),
    RequestType.CLARIFICATION: Template(
        id=RequestType.CLARIFICATION,
        name="Clarification",
        description="Resolve explicitly missing or inconsistent details in an existing request.",
        questions=[
            Question(id="missing_figures", label="Provide the missing figures named in the source request, with units and period.", dataType="number", evidenceRule="reported"),
            Question(id="period_basis", label="Confirm whether the figures are calendar-year or financial-year values.", evidenceRule="reported"),
            Question(id="source_document", label="Identify the document or person supporting the supplied figures.", evidenceRule="reported"),
        ],
    ),
    RequestType.RENEWAL_CHANGES: Template(
        id=RequestType.RENEWAL_CHANGES,
        name="Renewal changes",
        description="Ask whether approved prior facts changed; silence is never treated as no change.",
        questions=[
            Question(id="changed_activity", label="Has the business activity changed since the prior policy period?", evidenceRule="reported"),
            Question(id="changed_turnover", label="Has turnover changed? If yes, provide the current figure, period, and currency.", dataType="number", unitsHint="currency", evidenceRule="reported"),
            Question(id="changed_locations", label="Have locations, occupancy, or operations materially changed?", evidenceRule="reported"),
        ],
    ),
}
