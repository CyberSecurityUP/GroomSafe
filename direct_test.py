#!/usr/bin/env python3
"""
Direct server test (bypasses HTTP clients)
Tests by importing the API directly
"""

import sys
from pathlib import Path
import json

# Add to path
sys.path.insert(0, str(Path(__file__).parent / "groomsafe"))

from core.data_models import Conversation
from core.risk_scoring import RiskScoringEngine
from core.humanshield import HumanShieldLayer
from core.explainability import ExplainabilityEngine

print("=" * 70)
print("GROOMSAFE DIRECT TEST (No HTTP)")
print("=" * 70)
print()

# Load a test conversation
data_file = Path("groomsafe/data/synthetic/high_risk_conversation.json")
with open(data_file) as f:
    conv_data = json.load(f)

conversation = Conversation(**conv_data)
print(f"✅ Loaded conversation: {len(conversation.messages)} messages")
print()

# Initialize components
risk_engine = RiskScoringEngine()
humanshield = HumanShieldLayer()
explainer = ExplainabilityEngine()

# Assess risk
print("Running risk assessment...")
assessment = risk_engine.assess_risk(conversation)
print()

print("=" * 70)
print("RISK ASSESSMENT RESULTS")
print("=" * 70)
print(f"Risk Score:      {assessment.grooming_risk_score:.1f}/100")
print(f"Risk Level:      {assessment.risk_level.value.upper()}")
print(f"Confidence:      {assessment.confidence_level:.3f}")
print(f"Stage:           {assessment.current_stage.value.replace('_', ' ').title()}")
print(f"Human Review:    {'✅ REQUIRED' if assessment.requires_human_review else 'Not required'}")
print()

# Get features
features = risk_engine.feature_extractor.extract_features(conversation)

# HUMANSHIELD summary
safe_summary = humanshield.create_safe_summary(
    conversation,
    assessment,
    features,
    exposure_level="minimal"
)

print("=" * 70)
print("HUMANSHIELD PROTECTION SUMMARY")
print("=" * 70)
print(f"Behavioral Cluster: {safe_summary.behavioral_cluster}")
print(f"Temporal Pattern:   {safe_summary.temporal_pattern_summary}")
print()
print("Key Risk Indicators:")
for indicator in safe_summary.key_risk_indicators:
    print(f"  ⚠️  {indicator}")
print()

# Explanation
explanation = explainer.generate_explanation(assessment, features, conversation)

print("=" * 70)
print("TOP CONTRIBUTING FEATURES")
print("=" * 70)
for i, contrib in enumerate(explanation['feature_analysis']['top_contributors'][:5], 1):
    print(f"{i}. {contrib['feature']}")
    print(f"   Value: {contrib['value']:.3f} | Contribution: {contrib['contribution']:.3f}")
    print(f"   {contrib['description']}")
    print()

print("=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)
for rec in explanation['recommendations'][:5]:
    print(f"  • {rec}")
print()

print("=" * 70)
print("✅ TEST COMPLETE - All systems operational!")
print("=" * 70)
print()
print("API Server Info:")
print("  URL: http://localhost:8090")
print("  Docs: http://localhost:8090/docs")
print("  Status: Ready to start")
print()
print("To test via HTTP, disable Burp Suite proxy or access via browser.")
