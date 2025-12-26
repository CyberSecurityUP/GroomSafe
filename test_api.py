#!/usr/bin/env python3
"""
Quick API test script for GROOMSAFE
Tests the running API server
"""

import requests
import json
from pathlib import Path

API_BASE = "http://localhost:8090"

def test_health():
    """Test health endpoint"""
    print("=" * 60)
    print("Testing /health endpoint")
    print("=" * 60)

    response = requests.get(f"{API_BASE}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Test root endpoint"""
    print("=" * 60)
    print("Testing / root endpoint")
    print("=" * 60)

    response = requests.get(f"{API_BASE}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print()

def test_assess_conversation(dataset_name="moderate_risk"):
    """Test conversation assessment"""
    print("=" * 60)
    print(f"Testing /api/v1/assess with {dataset_name} dataset")
    print("=" * 60)

    # Load synthetic conversation
    data_file = Path(f"groomsafe/data/synthetic/{dataset_name}_conversation.json")

    if not data_file.exists():
        print(f"Error: Dataset not found: {data_file}")
        return

    with open(data_file) as f:
        conversation = json.load(f)

    # Make assessment request
    payload = {
        "conversation": conversation,
        "exposure_level": "minimal",
        "analyst_id": "test_analyst_001"
    }

    response = requests.post(
        f"{API_BASE}/api/v1/assess",
        json=payload
    )

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()

        # Print key results
        risk = result['risk_assessment']
        print(f"\n✅ RISK ASSESSMENT")
        print(f"  Risk Score: {risk['grooming_risk_score']:.1f}/100")
        print(f"  Risk Level: {risk['risk_level'].upper()}")
        print(f"  Stage: {risk['current_stage'].replace('_', ' ').title()}")
        print(f"  Confidence: {risk['confidence_level']:.3f}")
        print(f"  Human Review Required: {risk['requires_human_review']}")

        # Print behavioral summary
        summary = result['humanshield_summary']
        print(f"\n🛡️ HUMANSHIELD SUMMARY")
        print(f"  Behavioral Cluster: {summary['behavioral_cluster']}")
        print(f"  Temporal Pattern: {summary['temporal_pattern_summary']}")

        print(f"\n  Key Risk Indicators:")
        for indicator in summary['key_risk_indicators'][:5]:
            print(f"    - {indicator}")

        # Print top features
        print(f"\n📊 TOP CONTRIBUTING FEATURES")
        for contrib in result['explanation']['feature_analysis']['top_contributors'][:3]:
            print(f"  - {contrib['feature']}: {contrib['value']:.3f}")
    else:
        print(f"Error: {response.text}")

    print()

def test_stage_description():
    """Test stage description endpoint"""
    print("=" * 60)
    print("Testing /api/v1/stage/description endpoint")
    print("=" * 60)

    stage = "emotional_dependency"
    response = requests.get(f"{API_BASE}/api/v1/stage/description/{stage}")

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nStage: {result['stage'].replace('_', ' ').title()}")
        print(f"\nDescription:\n{result['description']}")
        print(f"\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  - {rec}")
    else:
        print(f"Error: {response.text}")

    print()

def test_analyst_safety():
    """Test analyst safety check"""
    print("=" * 60)
    print("Testing /api/v1/analyst/check-safety endpoint")
    print("=" * 60)

    response = requests.post(
        f"{API_BASE}/api/v1/analyst/check-safety",
        params={
            "analyst_id": "test_analyst_001",
            "risk_level": "moderate"
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print()

def main():
    """Run all tests"""
    print("\n" + "🚀 " * 30)
    print("GROOMSAFE API TEST SUITE")
    print("🚀 " * 30 + "\n")

    try:
        # Basic endpoints
        test_health()
        test_root()

        # Stage description
        test_stage_description()

        # Analyst safety
        test_analyst_safety()

        # Conversation assessments
        test_assess_conversation("low_risk")
        test_assess_conversation("moderate_risk")
        test_assess_conversation("high_risk")
        test_assess_conversation("critical_risk")

        print("=" * 60)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API server")
        print("Make sure the server is running on http://localhost:8090")
        print("Start it with: cd groomsafe/api && python3 api.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()
