from datetime import datetime
from typing import Any, Dict, List, Optional, Union, cast

from pydantic import BaseModel, ConfigDict, Field


class Assessment(BaseModel):
    """Details of an assessment."""

    id: str = Field(alias="AssessmentId")
    name: str = Field(alias="AssessmentName")
    description: str = Field(alias="Description")
    status: str = Field(alias="Status")
    assessment_arn: str = Field(alias="AssessmentArn")
    lenses: List[str] = Field(alias="Lenses")
    total_questions: int = Field(alias="TotalQuestions")
    answered_questions: int = Field(alias="AnsweredQuestions")
    created_at: Optional[datetime] = Field(None, alias="CreatedAt")
    updated_at: Optional[datetime] = Field(None, alias="UpdatedAt")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListAssessmentsOutput(BaseModel):
    """Output of list_assessments operation."""

    assessments: List[Assessment] = Field(alias="Assessments")
    next_page_token: Optional[str] = Field(None, alias="NextPageToken")
    # Keep these fields for backward compatibility
    page_number: Optional[int] = Field(None, alias="PageNumber")
    has_more: Optional[bool] = Field(None, alias="HasMore")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class CreateAssessmentInput(BaseModel):
    """Input for creating an assessment.

    According to the server-side schema, Scope can be one of two formats:
    1. ScopeAcc: {"Project": {}, "Accounts": [{"AccountNumber": "123", "Regions": ["us-east-1"]}]}
    2. ScopeProj: {"Project": {"ProjectId": "123", "Applications": ["app1"]}, "Accounts": ["123"]}
    """

    name: str = Field(alias="AssessmentName")
    description: str = Field(alias="Description")
    review_owner: str = Field(alias="ReviewOwner")
    scope: Dict[str, Any] = Field(alias="Scope")
    lenses: Optional[List[str]] = Field(default=[], alias="Lenses")
    tags: Optional[Dict[str, Any]] = Field(default={}, alias="Tags")
    region_code: str = Field(alias="RegionCode")
    environment: str = Field(alias="Environment")
    hosted_account_number: Optional[str] = Field(
        default=None, alias="HostedAccountNumber"
    )
    diagram_url: Optional[str] = Field(default=None, alias="DiagramURL")
    industry_type: Optional[str] = Field(default=None, alias="IndustryType")
    industry: Optional[str] = Field(default=None, alias="Industry")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class GetAssessmentOutput(BaseModel):
    """Output of get_assessment operation."""

    id: str = Field(alias="AssessmentId")
    name: str = Field(alias="AssessmentName")
    description: str = Field(alias="Description")
    status: str = Field(alias="Status")
    assessment_arn: str = Field(alias="AssessmentArn")
    created_at: datetime = Field(alias="CreatedAt")
    updated_at: datetime = Field(alias="UpdatedAt")
    answered_questions: int = Field(alias="AnsweredQuestions")
    total_questions: int = Field(alias="TotalQuestions")
    lenses: List[str] = Field(alias="Lenses")
    owner: str = Field(alias="Owner")
    diagram_url: Optional[str] = Field(None, alias="DiagramURL")
    environment: str = Field(alias="Environment")
    improvement_status: str = Field(alias="ImprovementStatus")
    in_sync: int = Field(alias="InSync")
    industry: Optional[str] = Field(None, alias="Industry")
    industry_type: Optional[str] = Field(None, alias="IndustryType")
    region_code: str = Field(alias="RegionCode")
    scope: List[Dict[str, Any]] = Field(alias="Scope")
    risk_counts: Dict[str, Any] = Field(alias="RiskCounts")
    lens_alias: str = Field(alias="LensAlias")
    lens_arn: str = Field(alias="LensArn")
    lens_version: str = Field(alias="LensVersion")
    lens_name: str = Field(alias="LensName")
    lens_status: str = Field(alias="LensStatus")
    aws_updated_at: str = Field(
        alias="AWSUpdatedAt"
    )  # Changed to str to handle timezone format

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class CreateAssessmentOutput(BaseModel):
    """Output of create_assessment operation.

    According to the OpenAPI specification, this only returns the AssessmentId and AssessmentArn.
    """

    # Fields from the OpenAPI spec
    id: str = Field(alias="AssessmentId")
    assessment_arn: str = Field(alias="AssessmentArn")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class Question(BaseModel):
    """Details of an assessment question."""

    id: str = Field(alias="QuestionId")
    title: str = Field(alias="QuestionTitle")
    pillar_id: str = Field(alias="PillarId")
    risk: Optional[str] = Field(None, alias="Risk")
    reason: Optional[str] = Field(None, alias="Reason")

    # These fields are not in the API response, but we'll add them with default values
    # to maintain compatibility with our code
    description: Optional[str] = Field("", alias="QuestionDescription")
    pillar_name: Optional[str] = Field("", alias="PillarName")
    is_answered: Optional[bool] = Field(False, alias="IsAnswered")
    choices: Optional[List[Dict[str, Any]]] = Field(None, alias="Choices")
    selected_choices: Optional[List[str]] = Field(None, alias="SelectedChoices")
    notes: Optional[str] = Field(None, alias="Notes")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListQuestionsOutput(BaseModel):
    """Output of list_questions operation."""

    questions: List[Question] = Field(alias="Questions")

    # These fields are not in the API response, but we'll add them with default values
    # to maintain compatibility with our code
    total_questions: Optional[int] = Field(0, alias="TotalQuestions")
    answered_questions: Optional[int] = Field(0, alias="AnsweredQuestions")
    pillar_id: Optional[str] = Field("", alias="PillarId")
    pillar_name: Optional[str] = Field("", alias="PillarName")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # If these fields aren't in the API response, calculate them from the questions
        if self.questions and not self.pillar_id and len(self.questions) > 0:
            self.pillar_id = self.questions[0].pillar_id

        # Calculate total and answered questions
        if self.questions:
            self.total_questions = len(self.questions)
            self.answered_questions = sum(
                1 for q in self.questions if q.risk and q.risk != "UNANSWERED"
            )

            # Set is_answered based on risk
            for question in self.questions:
                question.is_answered = (
                    question.risk is not None and question.risk != "UNANSWERED"
                )


class GetQuestionOutput(BaseModel):
    """Output of get_question operation."""

    # Fields directly from the API response
    title: str = Field(alias="QuestionTitle")
    description: str = Field(alias="QuestionDescription")
    pillar_id: str = Field(alias="PillarId")
    choices: List[Dict[str, Any]] = Field(alias="Choices")
    is_applicable: bool = Field(alias="IsApplicable")
    risk: Optional[str] = Field(None, alias="Risk")
    reason: Optional[str] = Field(None, alias="Reason")
    helpful_resource_url: Optional[str] = Field(None, alias="HelpfulResourceUrl")
    improvement_plan_url: Optional[str] = Field(None, alias="ImprovementPlanUrl")
    choice_answers: List[Union[str, Dict[str, Any]]] = Field(
        default_factory=list, alias="ChoiceAnswers"
    )

    # Fields we compute or add for convenience
    id: Optional[str] = None  # Will be set from the question_id parameter
    pillar_name: Optional[str] = None  # Will be set if available in the response
    notes: Optional[str] = Field(None, alias="Notes")  # May be in API response
    is_answered: bool = False  # Computed based on risk

    # For backward compatibility
    # Use the same type as choice_answers to avoid type errors
    selected_choices: List[str] = Field(
        default_factory=list
    )  # Alias for choice_answers

    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # Set is_answered based on risk
        self.is_answered = (
            self.risk is not None and self.risk != "UNANSWERED" and self.risk != ""
        )

        # Process choice_answers to handle both string and dictionary formats
        processed_choice_answers: List[str] = []
        for choice in self.choice_answers:
            if isinstance(choice, str):
                processed_choice_answers.append(choice)
            elif isinstance(choice, dict) and "ChoiceId" in choice:
                processed_choice_answers.append(choice["ChoiceId"])

        # Use type casting to satisfy mypy
        self.choice_answers = cast(
            List[Union[str, Dict[str, Any]]], processed_choice_answers
        )

        # Set selected_choices as an alias for choice_answers
        self.selected_choices = processed_choice_answers


class ChoiceStatus(BaseModel):
    """Status of a choice in an answer."""

    status: str = Field("SELECTED", alias="Status")

    model_config = ConfigDict(extra="allow")


class AnswerQuestionInput(BaseModel):
    """Input for answering a question."""

    lens_alias: str = Field("wellarchitected", alias="LensAlias")
    choice_updates: Dict[str, ChoiceStatus] = Field(
        default_factory=dict, alias="ChoiceUpdates"
    )
    notes: Optional[str] = Field(None, alias="Notes")
    is_applicable: bool = Field(True, alias="IsApplicable")
    reason: str = Field("NONE", alias="Reason")

    # For backward compatibility - excluded from model_dump
    selected_choices: Optional[List[str]] = Field(None, exclude=True)
    risk: Optional[str] = Field(
        None, exclude=True
    )  # Risk is no longer used in the new API format

    # Allow extra fields
    model_config = ConfigDict(extra="allow")

    def __init__(self, **data: Any) -> None:
        # Validate reason is one of the allowed values
        valid_reasons = [
            "OUT_OF_SCOPE",
            "BUSINESS_PRIORITIES",
            "ARCHITECTURE_CONSTRAINTS",
            "OTHER",
            "NONE",
        ]
        if "reason" in data or "Reason" in data:
            reason = data.get("reason") or data.get("Reason")
            if reason and reason not in valid_reasons:
                data["Reason"] = "OTHER"

        super().__init__(**data)


class AnswerQuestionOutput(BaseModel):
    """Output of answer_question operation.

    The API returns a success message with status and message fields.
    """

    # Fields directly from the API response
    status: str = Field(alias="Status")
    message: str = Field(alias="Message")

    id: Optional[str] = None

    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class Finding(BaseModel):
    """Details of a finding."""

    finding_id: str = Field(alias="FindingId")
    resource_id: str = Field(alias="ResourceId")
    resource_type: str = Field(alias="ResourceType")
    account_number: str = Field(alias="AccountNumber")
    region_code: str = Field(alias="RegionCode")
    check_id: str = Field(alias="CheckId")
    recommendation: str = Field(alias="Recommendation")
    remediation: bool = Field(alias="Remediation")
    created_at: str = Field(alias="CreatedAt")
    question_id: str = Field(alias="QuestionId")
    question: str = Field(alias="Question")
    pillar_id: str = Field(alias="PillarId")
    severity: str = Field(alias="Severity")
    status: str = Field(alias="Status")
    title: str = Field(alias="Title")
    description: str = Field(alias="Description")
    best_practice_id: str = Field(alias="BestPracticeId")
    best_practice: str = Field(alias="BestPractice")
    best_practice_risk: str = Field(alias="BestPracticeRisk")
    # Allow extra fields
    model_config = ConfigDict(extra="allow")


class ListFindingsOutput(BaseModel):
    """Output of list_findings operation."""

    records: List[Finding] = Field(alias="Records", default=[])
    next_page_token: Optional[str] = Field(None, alias="NextPageToken")

    # Allow extra fields
    model_config = ConfigDict(extra="allow")
