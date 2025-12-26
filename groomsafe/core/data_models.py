"""
GROOMSAFE Data Models
Clean, auditable data structures for behavioral analysis and risk assessment
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class SenderRole(str, Enum):
    """Role of message sender in conversation"""
    ADULT = "adult"
    MINOR = "minor"
    UNKNOWN = "unknown"


class GroomingStage(str, Enum):
    """Grooming progression stages - abstract and non-sexual"""
    INITIAL_CONTACT = "initial_contact"
    TRUST_BUILDING = "trust_building"
    EMOTIONAL_DEPENDENCY = "emotional_dependency"
    ISOLATION_ATTEMPTS = "isolation_attempts"
    ESCALATION_RISK = "escalation_risk"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    """Risk level classification"""
    MINIMAL = "minimal"  # 0-20
    LOW = "low"  # 21-40
    MODERATE = "moderate"  # 41-60
    HIGH = "high"  # 61-80
    CRITICAL = "critical"  # 81-100


class Message(BaseModel):
    """
    Individual message in a conversation
    Contains only abstracted, non-explicit content
    """
    message_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime
    sender_role: SenderRole
    abstracted_text: str = Field(
        ...,
        description="Sanitized, abstracted representation of message content"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Non-sensitive metadata (e.g., message_length, time_of_day)"
    )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class Conversation(BaseModel):
    """
    Sequence of messages representing an interaction
    Anonymized and sanitized for analysis
    """
    conversation_id: UUID = Field(default_factory=uuid4)
    messages: List[Message]
    start_time: datetime
    end_time: Optional[datetime] = None
    platform_type: Optional[str] = Field(
        None,
        description="Type of platform (e.g., 'social_media', 'gaming', 'messaging')"
    )
    is_synthetic: bool = Field(
        default=False,
        description="Flag indicating if this is synthetic data for research/testing"
    )

    @validator('messages')
    def validate_messages(cls, v):
        if len(v) < 1:
            raise ValueError("Conversation must contain at least one message")
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class BehavioralFeatures(BaseModel):
    """
    Extracted behavioral signals - no content analysis
    Focus on temporal, relational, and behavioral patterns
    """
    conversation_id: UUID

    # Temporal patterns
    contact_frequency_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Escalation in contact frequency over time"
    )
    persistence_after_nonresponse: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Continued messaging despite no response"
    )
    time_of_day_irregularity: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Messaging at unusual hours (late night, early morning)"
    )

    # Relational patterns
    emotional_dependency_indicators: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Patterns suggesting emotional manipulation or dependency building"
    )
    isolation_pressure: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Attempts to isolate target from others"
    )
    secrecy_pressure: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Requests for secrecy or privacy"
    )

    # Platform behavior
    platform_migration_attempts: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Attempts to move conversation to other platforms"
    )

    # Linguistic patterns
    tone_shift_score: float = Field(
        0.0, ge=0.0, le=1.0,
        description="Changes in linguistic tone over conversation timeline"
    )

    # Metadata
    extraction_timestamp: datetime = Field(default_factory=datetime.utcnow)
    feature_version: str = Field(
        "1.0.0",
        description="Version of feature extraction algorithm"
    )

    class Config:
        protected_namespaces = ()
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class FeatureContribution(BaseModel):
    """Contribution of individual features to risk score"""
    feature_name: str
    value: float
    contribution_weight: float
    description: str


class LLMAnalysisResult(BaseModel):
    """LLM-enhanced analysis result (optional)"""
    provider: str  # ollama, gemini, claude, chatgpt
    model: str
    severity_assessment: str  # low, moderate, high, critical
    confidence: float = Field(ge=0.0, le=1.0)
    risk_factors: List[str] = Field(default_factory=list)
    grooming_indicators: List[str] = Field(default_factory=list)
    explanation: str = ""
    recommended_actions: List[str] = Field(default_factory=list)


class RiskAssessment(BaseModel):
    """
    Risk assessment output - explainable and auditable
    Signals risk, does not assign guilt
    """
    assessment_id: UUID = Field(default_factory=uuid4)
    conversation_id: UUID

    # Risk metrics
    grooming_risk_score: float = Field(
        ..., ge=0.0, le=100.0,
        description="Overall grooming risk score (0-100)"
    )
    confidence_level: float = Field(
        ..., ge=0.0, le=1.0,
        description="Confidence in the risk assessment"
    )
    risk_level: RiskLevel

    # Progression analysis
    current_stage: GroomingStage
    stage_confidence: float = Field(
        ..., ge=0.0, le=1.0,
        description="Confidence in stage classification"
    )

    # Explainability
    feature_contributions: List[FeatureContribution]
    reasoning_summary: str = Field(
        ...,
        description="Human-readable explanation of the assessment"
    )

    # Metadata
    assessment_timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_version: str = Field(
        "1.0.0",
        description="Version of risk scoring model"
    )
    requires_human_review: bool = Field(
        default=False,
        description="Flag indicating human review is recommended"
    )

    # LLM-enhanced analysis (optional)
    llm_enabled: bool = Field(
        default=False,
        description="Whether LLM analysis was used"
    )
    llm_analysis: Optional[LLMAnalysisResult] = Field(
        None,
        description="LLM-enhanced analysis results"
    )

    @validator('risk_level', always=True)
    def determine_risk_level(cls, v, values):
        """Auto-determine risk level from score if not provided"""
        if 'grooming_risk_score' in values:
            score = values['grooming_risk_score']
            if score <= 20:
                return RiskLevel.MINIMAL
            elif score <= 40:
                return RiskLevel.LOW
            elif score <= 60:
                return RiskLevel.MODERATE
            elif score <= 80:
                return RiskLevel.HIGH
            else:
                return RiskLevel.CRITICAL
        return v

    class Config:
        protected_namespaces = ()
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class AuditLogEntry(BaseModel):
    """
    Audit log entry for decision tracking and accountability
    Ensures legal defensibility and transparency
    """
    log_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    conversation_id: UUID
    assessment_id: Optional[UUID] = None

    # Action details
    action_type: str = Field(
        ...,
        description="Type of action (e.g., 'assessment_created', 'human_review_triggered')"
    )
    actor: str = Field(
        ...,
        description="System component or user that performed action"
    )

    # Context
    risk_score: Optional[float] = None
    risk_level: Optional[RiskLevel] = None
    stage: Optional[GroomingStage] = None

    # Audit trail
    decision_rationale: str
    model_version: str

    # Additional data
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        protected_namespaces = ()
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class HumanShieldSummary(BaseModel):
    """
    Abstracted, analyst-safe representation of conversation
    No raw content, no disturbing material
    """
    conversation_id: UUID

    # Safe representations
    message_count: int
    conversation_duration_hours: float
    temporal_pattern_summary: str
    behavioral_cluster: str = Field(
        ...,
        description="High-level behavioral pattern category"
    )

    # Risk indicators (abstract)
    key_risk_indicators: List[str] = Field(
        default_factory=list,
        description="List of abstract risk indicators (no explicit content)"
    )

    # Timeline data (for visualization)
    timeline_events: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Abstracted timeline events for graphical display"
    )

    # Exposure control
    exposure_level: str = Field(
        "minimal",
        description="Level of detail exposure (minimal, moderate, detailed)"
    )
    analyst_safety_certified: bool = Field(
        default=True,
        description="Confirms content is safe for analyst review"
    )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
