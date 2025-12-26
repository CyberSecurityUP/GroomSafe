# GROOMSAFE Quick Start Guide

Get up and running with GROOMSAFE in 5 minutes.

## Installation

```bash
# 1. Navigate to project directory
cd GROOMSAFE

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic test data
cd groomsafe
python3 data/synthetic/generate_synthetic_data.py
```

## Quick Test

### Option 1: Run Example Analysis

```bash
# From groomsafe/ directory
python3 examples/example_usage.py
```

This will analyze all four synthetic datasets (low, moderate, high, critical risk) and show you complete assessment workflows.

### Option 2: Start API Server

```bash
# From groomsafe/api/ directory
python3 api.py
```

Then visit:
- API Docs: http://localhost:8090/docs
- Health Check: http://localhost:8090/health

### Option 3: Python Script

Create `test_groomsafe.py`:

```python
import json
from pathlib import Path
import sys

# Add groomsafe to path
sys.path.insert(0, str(Path(__file__).parent / "groomsafe"))

from core.data_models import Conversation
from core.risk_scoring import RiskScoringEngine
from core.humanshield import HumanShieldLayer
from core.explainability import ExplainabilityEngine

# Load synthetic conversation
with open("groomsafe/data/synthetic/high_risk_conversation.json") as f:
    conv_data = json.load(f)

conversation = Conversation(**conv_data)

# Assess risk
risk_engine = RiskScoringEngine()
assessment = risk_engine.assess_risk(conversation)

print(f"Risk Score: {assessment.grooming_risk_score:.1f}/100")
print(f"Risk Level: {assessment.risk_level.value.upper()}")
print(f"Stage: {assessment.current_stage.value}")
print(f"Requires Review: {assessment.requires_human_review}")

# Get safe summary for analyst
humanshield = HumanShieldLayer()
features = risk_engine.feature_extractor.extract_features(conversation)
safe_summary = humanshield.create_safe_summary(
    conversation,
    assessment,
    features
)

print(f"\nBehavioral Cluster: {safe_summary.behavioral_cluster}")
print("\nKey Risk Indicators:")
for indicator in safe_summary.key_risk_indicators:
    print(f"  - {indicator}")

# Get explanation
explainer = ExplainabilityEngine()
explanation = explainer.generate_explanation(
    assessment,
    features,
    conversation
)

print(f"\nExplanation: {explanation['summary']}")
```

Run it:
```bash
python3 test_groomsafe.py
```

## API Usage

### Assess a Conversation

```bash
curl -X POST "http://localhost:8090/api/v1/assess" \
  -H "Content-Type: application/json" \
  -d @groomsafe/data/synthetic/moderate_risk_conversation.json
```

Or using Python `requests`:

```python
import requests
import json

# Load conversation
with open("groomsafe/data/synthetic/moderate_risk_conversation.json") as f:
    conversation = json.load(f)

# Assess via API
response = requests.post(
    "http://localhost:8090/api/v1/assess",
    json={
        "conversation": conversation,
        "exposure_level": "minimal",
        "analyst_id": "analyst_001"
    }
)

result = response.json()
print(f"Risk Score: {result['risk_assessment']['grooming_risk_score']}")
```

## Understanding the Output

### Risk Assessment
```json
{
  "grooming_risk_score": 75.3,      // 0-100 scale
  "risk_level": "high",              // minimal, low, moderate, high, critical
  "current_stage": "isolation_attempts",
  "requires_human_review": true
}
```

### Behavioral Features
```json
{
  "contact_frequency_score": 0.65,
  "persistence_after_nonresponse": 0.72,
  "emotional_dependency_indicators": 0.58,
  // ... other features
}
```

### HUMANSHIELD Summary (Safe for Analysts)
```json
{
  "behavioral_cluster": "High Risk: Isolation Tactics",
  "key_risk_indicators": [
    "Escalating contact pattern detected",
    "Isolation attempt signals",
    "Secrecy or privacy pressure"
  ]
}
```

## Next Steps

1. **Read the full README**: `README.md`
2. **Explore the code**: Start with `groomsafe/core/`
3. **Review synthetic data**: `groomsafe/data/synthetic/`
4. **Check API docs**: http://localhost:8090/docs
5. **Read contributing guide**: `CONTRIBUTING.md`

## Common Issues

### Import Errors
Make sure you're in the right directory and have installed dependencies:
```bash
pip install -r requirements.txt
```

### No Synthetic Data
Generate it first:
```bash
cd groomsafe
python3 data/synthetic/generate_synthetic_data.py
```

### Port Already in Use
Change the port in `api.py`:
```python
uvicorn.run("api:app", host="0.0.0.0", port=8090)  # Default port
```

## Help

- Documentation: See `README.md`
- Issues: Check GitHub Issues
- Questions: Open a new issue with `question` label

## Remember

This is a **research prototype** for:
- ✅ Child safety research
- ✅ Education and training
- ✅ Platform safety development
- ✅ Academic publication

This is NOT for:
- ❌ Production deployment without validation
- ❌ Surveillance without authorization
- ❌ Making decisions without human review

Always use responsibly and ethically!
