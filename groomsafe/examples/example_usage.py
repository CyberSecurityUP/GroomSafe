"""
GROOMSAFE Example Usage
Demonstrates how to use the GROOMSAFE system for behavioral risk assessment
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.data_models import Conversation
from core.feature_extraction import BehavioralFeatureExtractor
from core.progression_model import GroomingProgressionModel
from core.risk_scoring import RiskScoringEngine
from core.humanshield import HumanShieldLayer
from core.explainability import ExplainabilityEngine
from core.audit_log import AuditLogger


def analyze_conversation(conversation_path: str):
    """
    Complete example of analyzing a conversation

    Args:
        conversation_path: Path to conversation JSON file
    """
    print("=" * 80)
    print("GROOMSAFE RISK ASSESSMENT EXAMPLE")
    print("=" * 80)
    print()

    # Load conversation
    print(f"Loading conversation from: {conversation_path}")
    with open(conversation_path, 'r') as f:
        conversation_data = json.load(f)

    conversation = Conversation(**conversation_data)
    print(f"✓ Loaded conversation with {len(conversation.messages)} messages")
    print()

    # Initialize components
    print("Initializing GROOMSAFE components...")
    feature_extractor = BehavioralFeatureExtractor()
    progression_model = GroomingProgressionModel()
    risk_engine = RiskScoringEngine()
    humanshield = HumanShieldLayer()
    explainability = ExplainabilityEngine()
    audit_logger = AuditLogger()
    print("✓ All components initialized")
    print()

    # Extract features
    print("-" * 80)
    print("STEP 1: Extracting Behavioral Features")
    print("-" * 80)
    features = feature_extractor.extract_features(conversation)

    print(f"Contact Frequency Score: {features.contact_frequency_score:.3f}")
    print(f"Persistence After Non-Response: {features.persistence_after_nonresponse:.3f}")
    print(f"Time Irregularity: {features.time_of_day_irregularity:.3f}")
    print(f"Emotional Dependency: {features.emotional_dependency_indicators:.3f}")
    print(f"Isolation Pressure: {features.isolation_pressure:.3f}")
    print(f"Secrecy Pressure: {features.secrecy_pressure:.3f}")
    print(f"Platform Migration: {features.platform_migration_attempts:.3f}")
    print(f"Tone Shift: {features.tone_shift_score:.3f}")
    print()

    # Classify stage
    print("-" * 80)
    print("STEP 2: Classifying Progression Stage")
    print("-" * 80)
    stage, stage_confidence = progression_model.classify_stage(features, conversation)

    print(f"Current Stage: {stage.value.replace('_', ' ').title()}")
    print(f"Stage Confidence: {stage_confidence:.3f}")
    print()
    print("Stage Description:")
    print(progression_model.get_stage_description(stage))
    print()

    # Calculate risk score
    print("-" * 80)
    print("STEP 3: Calculating Risk Score")
    print("-" * 80)
    risk_assessment = risk_engine.assess_risk(conversation)

    print(f"Risk Score: {risk_assessment.grooming_risk_score:.1f}/100")
    print(f"Risk Level: {risk_assessment.risk_level.value.upper()}")
    print(f"Confidence: {risk_assessment.confidence_level:.3f}")
    print(f"Human Review Required: {'YES' if risk_assessment.requires_human_review else 'No'}")
    print()

    # Generate HUMANSHIELD summary
    print("-" * 80)
    print("STEP 4: Creating HUMANSHIELD Safe Summary")
    print("-" * 80)
    safe_summary = humanshield.create_safe_summary(
        conversation,
        risk_assessment,
        features,
        exposure_level="minimal"
    )

    print(f"Behavioral Cluster: {safe_summary.behavioral_cluster}")
    print(f"Temporal Pattern: {safe_summary.temporal_pattern_summary}")
    print()
    print("Key Risk Indicators:")
    for indicator in safe_summary.key_risk_indicators:
        print(f"  - {indicator}")
    print()

    # Generate explanation
    print("-" * 80)
    print("STEP 5: Generating Explainability Report")
    print("-" * 80)
    explanation = explainability.generate_explanation(
        risk_assessment,
        features,
        conversation
    )

    print("Summary:")
    print(explanation['summary'])
    print()

    print("Top Contributing Features:")
    for contrib in explanation['feature_analysis']['top_contributors'][:3]:
        print(f"  - {contrib['feature']}: {contrib['value']:.3f} (weight: {contrib['contribution']:.3f})")
        print(f"    {contrib['description']}")
    print()

    print("Recommendations:")
    for rec in explanation['recommendations'][:5]:
        print(f"  - {rec}")
    print()

    # Log to audit trail
    print("-" * 80)
    print("STEP 6: Logging to Audit Trail")
    print("-" * 80)
    audit_logger.log_assessment_created(
        risk_assessment,
        conversation.conversation_id,
        model_version="1.0.0"
    )

    if risk_assessment.requires_human_review:
        audit_logger.log_human_review_triggered(
            conversation.conversation_id,
            risk_assessment.assessment_id,
            f"Risk score {risk_assessment.grooming_risk_score:.1f} requires review",
            risk_assessment.grooming_risk_score,
            risk_assessment.risk_level
        )

    session_summary = audit_logger.get_session_summary()
    print(f"✓ Logged {session_summary['total_log_entries']} audit entries")
    print(f"Log file: {session_summary['log_file']}")
    print()

    # Generate visualization data
    print("-" * 80)
    print("STEP 7: Generating Visualization Data")
    print("-" * 80)
    viz_data = humanshield.generate_visualization_data(
        conversation,
        features,
        risk_assessment
    )

    print("Risk Score Gauge:")
    print(f"  Score: {viz_data['risk_score_gauge']['score']:.1f}")
    print(f"  Level: {viz_data['risk_score_gauge']['level']}")
    print(f"  Confidence: {viz_data['risk_score_gauge']['confidence']:.3f}")
    print()

    # Final summary
    print("=" * 80)
    print("ASSESSMENT COMPLETE")
    print("=" * 80)
    print(f"Conversation ID: {conversation.conversation_id}")
    print(f"Risk Score: {risk_assessment.grooming_risk_score:.1f}/100 ({risk_assessment.risk_level.value.upper()})")
    print(f"Stage: {stage.value.replace('_', ' ').title()}")
    print(f"Action Required: {'HUMAN REVIEW' if risk_assessment.requires_human_review else 'Continue Monitoring'}")
    print("=" * 80)
    print()


def main():
    """Run example analyses on all synthetic datasets"""
    synthetic_dir = Path(__file__).parent.parent / "data" / "synthetic"

    datasets = [
        ("LOW RISK", synthetic_dir / "low_risk_conversation.json"),
        ("MODERATE RISK", synthetic_dir / "moderate_risk_conversation.json"),
        ("HIGH RISK", synthetic_dir / "high_risk_conversation.json"),
        ("CRITICAL RISK", synthetic_dir / "critical_risk_conversation.json")
    ]

    for dataset_name, dataset_path in datasets:
        if dataset_path.exists():
            print(f"\n\n{'#' * 80}")
            print(f"# ANALYZING {dataset_name} EXAMPLE")
            print(f"{'#' * 80}\n")
            analyze_conversation(str(dataset_path))
            input("Press Enter to continue to next example...")
        else:
            print(f"Dataset not found: {dataset_path}")


if __name__ == "__main__":
    main()
