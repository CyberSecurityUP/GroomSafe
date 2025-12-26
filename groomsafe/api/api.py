"""
GROOMSAFE API
FastAPI-based REST API for risk assessment and analysis
"""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.data_models import (
    Conversation,
    Message,
    RiskAssessment,
    BehavioralFeatures,
    HumanShieldSummary,
    AuditLogEntry,
    GroomingStage,
    RiskLevel,
    LLMAnalysisResult
)
from core.feature_extraction import BehavioralFeatureExtractor
from core.progression_model import GroomingProgressionModel
from core.risk_scoring import RiskScoringEngine
from core.humanshield import HumanShieldLayer
from core.explainability import ExplainabilityEngine
from core.audit_log import AuditLogger
from core.llm_analyzer import (
    LLMAnalysisEngine,
    LLMConfig,
    LLMProvider
)


# API Request/Response Models
class AssessConversationRequest(BaseModel):
    """Request to assess a conversation"""
    conversation: Conversation
    exposure_level: str = Field(
        default="minimal",
        description="Analyst exposure level (minimal, moderate, detailed)"
    )
    analyst_id: Optional[str] = Field(
        default=None,
        description="Analyst ID for exposure tracking"
    )

    # LLM Configuration (optional)
    llm_enabled: bool = Field(
        default=False,
        description="Enable LLM-enhanced analysis"
    )
    llm_provider: Optional[str] = Field(
        default="ollama",
        description="LLM provider (ollama, gemini, claude, chatgpt)"
    )
    llm_model: Optional[str] = Field(
        default="llama-guard-3",
        description="LLM model to use"
    )
    llm_api_key: Optional[str] = Field(
        default=None,
        description="API key for external LLM providers"
    )


class AssessConversationResponse(BaseModel):
    """Response from conversation assessment"""
    risk_assessment: RiskAssessment
    behavioral_features: BehavioralFeatures
    humanshield_summary: HumanShieldSummary
    explanation: Dict[str, Any]


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str
    components: Dict[str, str]


# Initialize FastAPI app
app = FastAPI(
    title="GROOMSAFE API",
    description="Behavioral Grooming Detection and Investigator Protection System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
feature_extractor = BehavioralFeatureExtractor()
progression_model = GroomingProgressionModel()
risk_scoring_engine = RiskScoringEngine()
humanshield = HumanShieldLayer()
explainability_engine = ExplainabilityEngine()
audit_logger = AuditLogger()

# Mount static files for web interface
WEB_DIR = Path(__file__).parent.parent / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


@app.get("/", response_class=FileResponse)
async def root():
    """Serve web interface"""
    web_index = WEB_DIR / "index.html"
    if web_index.exists():
        return FileResponse(web_index)
    else:
        # Fallback to JSON response if web interface not found
        return {
            "service": "GROOMSAFE API",
            "version": "1.0.0",
            "status": "operational",
            "documentation": "/docs",
            "web_interface": "Not found - expected at groomsafe/web/index.html"
        }


@app.get("/api", response_model=dict)
async def api_root():
    """API root endpoint"""
    return {
        "service": "GROOMSAFE API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }


@app.get("/data/synthetic/{filename}")
async def serve_synthetic_data(filename: str):
    """Serve synthetic conversation data files"""
    # Security: only allow specific filenames
    allowed_files = [
        "low_risk_conversation.json",
        "moderate_risk_conversation.json",
        "high_risk_conversation.json",
        "critical_risk_conversation.json"
    ]

    if filename not in allowed_files:
        raise HTTPException(status_code=404, detail="File not found")

    # Construct path to synthetic data
    data_path = Path(__file__).parent.parent / "data" / "synthetic" / filename

    if not data_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(data_path)


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint
    Returns system status and component availability
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        components={
            "feature_extractor": "operational",
            "progression_model": "operational",
            "risk_scoring": "operational",
            "humanshield": "operational",
            "explainability": "operational",
            "audit_logger": "operational"
        }
    )


@app.get("/api/v1/llm/models")
async def get_llm_models():
    """
    Get recommended LLM models for each provider
    """
    return {
        "success": True,
        "models": LLMAnalysisEngine.get_recommended_models()
    }


@app.get("/api/v1/llm/status")
async def check_llm_status(provider: str = "ollama", model: str = "llama-guard-3"):
    """
    Check if LLM provider is available

    Args:
        provider: LLM provider (ollama, gemini, claude, chatgpt)
        model: Model name to check
    """
    try:
        config = LLMConfig(
            provider=LLMProvider(provider),
            model=model
        )
        engine = LLMAnalysisEngine(config)
        available = engine.is_available()

        return {
            "success": True,
            "provider": provider,
            "model": model,
            "available": available,
            "message": "LLM service is available" if available else "LLM service is not available. For Ollama, make sure it's installed and running."
        }
    except Exception as e:
        return {
            "success": False,
            "provider": provider,
            "model": model,
            "available": False,
            "error": str(e)
        }


@app.post("/api/v1/assess", response_model=AssessConversationResponse)
async def assess_conversation(request: AssessConversationRequest):
    """
    Assess a conversation for grooming risk

    This endpoint:
    1. Extracts behavioral features
    2. Classifies progression stage
    3. Calculates risk score
    4. Generates HUMANSHIELD summary
    5. Provides explainability
    6. Logs to audit trail

    Args:
        request: AssessConversationRequest with conversation data

    Returns:
        AssessConversationResponse with complete assessment
    """
    try:
        conversation = request.conversation

        # Validate conversation
        if len(conversation.messages) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conversation must contain at least one message"
            )

        # Check analyst safety if analyst_id provided
        if request.analyst_id:
            safety_check = humanshield.check_analyst_safety(
                request.analyst_id,
                "unknown"  # Will update after assessment
            )

            if not safety_check['safe_to_proceed']:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "message": "Analyst exposure limit exceeded",
                        "safety_check": safety_check
                    }
                )

        # Perform assessment
        risk_assessment = risk_scoring_engine.assess_risk(conversation)

        # LLM-enhanced analysis (optional)
        if request.llm_enabled:
            try:
                # Create LLM config
                llm_config = LLMConfig(
                    provider=LLMProvider(request.llm_provider or "ollama"),
                    model=request.llm_model or "llama-guard-3",
                    api_key=request.llm_api_key
                )

                # Create and run LLM analyzer
                llm_engine = LLMAnalysisEngine(llm_config)

                # Convert messages to dict format for LLM
                messages_dict = [
                    {
                        "sender_role": msg.sender_role.value,
                        "abstracted_text": msg.abstracted_text,
                        "timestamp": msg.timestamp.isoformat()
                    }
                    for msg in conversation.messages
                ]

                # Pass behavioral score to LLM for context
                llm_result = llm_engine.analyze(messages_dict, risk_assessment.grooming_risk_score)

                if llm_result:
                    # Add LLM analysis to risk assessment
                    risk_assessment.llm_enabled = True
                    risk_assessment.llm_analysis = LLMAnalysisResult(
                        provider=llm_result.provider,
                        model=llm_result.model,
                        severity_assessment=llm_result.severity_assessment,
                        confidence=llm_result.confidence,
                        risk_factors=llm_result.risk_factors,
                        grooming_indicators=llm_result.grooming_indicators,
                        explanation=llm_result.explanation,
                        recommended_actions=llm_result.recommended_actions
                    )
            except Exception as e:
                print(f"LLM analysis failed: {e}")
                # Continue without LLM enhancement

        # Extract features (already done in assess_risk, but we need them separately)
        behavioral_features = feature_extractor.extract_features(conversation)

        # Create HUMANSHIELD summary
        humanshield_summary = humanshield.create_safe_summary(
            conversation,
            risk_assessment,
            behavioral_features,
            exposure_level=request.exposure_level
        )

        # Generate explanation
        explanation = explainability_engine.generate_explanation(
            risk_assessment,
            behavioral_features,
            conversation
        )

        # Log to audit trail
        audit_logger.log_assessment_created(
            risk_assessment,
            conversation.conversation_id,
            model_version="1.0.0"
        )

        # Log human review trigger if needed
        if risk_assessment.requires_human_review:
            audit_logger.log_human_review_triggered(
                conversation.conversation_id,
                risk_assessment.assessment_id,
                trigger_reason=f"Risk score {risk_assessment.grooming_risk_score:.1f} requires review",
                risk_score=risk_assessment.grooming_risk_score,
                risk_level=risk_assessment.risk_level
            )

        # Update analyst exposure if tracked
        if request.analyst_id:
            humanshield.log_analyst_exposure(
                request.analyst_id,
                risk_assessment.risk_level.value,
                exposure_duration_minutes=1.0  # Estimate
            )

        return AssessConversationResponse(
            risk_assessment=risk_assessment,
            behavioral_features=behavioral_features,
            humanshield_summary=humanshield_summary,
            explanation=explanation
        )

    except HTTPException:
        raise
    except Exception as e:
        # Log error
        audit_logger.log_system_event(
            "assessment_error",
            f"Error during assessment: {str(e)}",
            metadata={"error_type": type(e).__name__}
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assessment failed: {str(e)}"
        )


@app.get("/api/v1/explanation/{assessment_id}", response_model=dict)
async def get_explanation(assessment_id: UUID):
    """
    Get detailed explanation for an assessment

    Args:
        assessment_id: Assessment identifier

    Returns:
        Detailed explanation dictionary
    """
    # In production, would retrieve from database
    # For now, return informational response
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Explanation retrieval requires persistent storage implementation"
    )


@app.get("/api/v1/audit/conversation/{conversation_id}", response_model=List[AuditLogEntry])
async def get_conversation_audit_trail(conversation_id: UUID):
    """
    Get audit trail for a conversation

    Args:
        conversation_id: Conversation identifier

    Returns:
        List of audit log entries
    """
    try:
        timeline = audit_logger.get_conversation_timeline(conversation_id)
        return timeline

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve audit trail: {str(e)}"
        )


@app.post("/api/v1/analyst/check-safety")
async def check_analyst_safety(analyst_id: str, risk_level: str = "moderate"):
    """
    Check analyst safety status

    Args:
        analyst_id: Analyst identifier
        risk_level: Risk level of case to review

    Returns:
        Safety check results
    """
    try:
        safety_check = humanshield.check_analyst_safety(analyst_id, risk_level)
        return safety_check

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Safety check failed: {str(e)}"
        )


@app.post("/api/v1/analyst/reset-session")
async def reset_analyst_session(analyst_id: str):
    """
    Reset analyst session after break

    Args:
        analyst_id: Analyst identifier

    Returns:
        Confirmation
    """
    try:
        humanshield.reset_analyst_session(analyst_id)
        return {
            "status": "success",
            "message": f"Session reset for analyst {analyst_id}",
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Session reset failed: {str(e)}"
        )


@app.get("/api/v1/visualization/{conversation_id}")
async def get_visualization_data(conversation_id: UUID):
    """
    Get visualization data for a conversation

    Args:
        conversation_id: Conversation identifier

    Returns:
        Visualization-ready data
    """
    # In production, would retrieve from database
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Visualization data retrieval requires persistent storage"
    )


@app.get("/api/v1/audit/compliance-report")
async def get_compliance_report(
    start_date: datetime,
    end_date: datetime
):
    """
    Generate compliance report for date range

    Args:
        start_date: Report start date
        end_date: Report end date

    Returns:
        Compliance metrics
    """
    try:
        report = audit_logger.generate_compliance_report(start_date, end_date)
        return report

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Compliance report generation failed: {str(e)}"
        )


@app.get("/api/v1/stage/description/{stage}")
async def get_stage_description(stage: str):
    """
    Get description of a grooming stage

    Args:
        stage: Stage name

    Returns:
        Stage description and recommendations
    """
    try:
        # Convert string to enum
        stage_enum = GroomingStage(stage)

        description = progression_model.get_stage_description(stage_enum)
        recommendations = progression_model.get_stage_recommendations(stage_enum)

        return {
            "stage": stage,
            "description": description,
            "recommendations": recommendations
        }

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stage: {stage}. Valid stages: {[s.value for s in GroomingStage]}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stage description: {str(e)}"
        )


@app.get("/api/v1/system/metrics")
async def get_system_metrics():
    """
    Get current system metrics

    Returns:
        System performance metrics
    """
    try:
        session_summary = audit_logger.get_session_summary()

        return {
            "session": session_summary,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system metrics: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    # Run server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8090,
        reload=True,
        log_level="info"
    )
