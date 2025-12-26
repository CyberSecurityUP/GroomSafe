# HUMANSHIELD + GROOMSAFE

## Behavioral Grooming Prevention & Investigator Protection Ecosystem

[![Author](https://img.shields.io/badge/Author-Joas%20Antonio-blue)](https://github.com/CyberSecurityUP)
[![GitHub](https://img.shields.io/badge/GitHub-CyberSecurityUP-black?logo=github)](https://github.com/CyberSecurityUP)
[![License](https://img.shields.io/badge/License-MIT%20with%20Ethical%20Use-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/CyberSecurityUP/GROOMSAFE)

**Author:** Joas Antonio ([@CyberSecurityUP](https://github.com/CyberSecurityUP))

---

## Overview

**HUMANSHIELD + GROOMSAFE** is a research-oriented, ethically grounded safety platform designed to detect early grooming patterns and protect investigators from psychological harm. This system combines behavioral analysis with psychological safety mechanisms to create a comprehensive child safety framework.

### Core Pillars

#### 🛡️ GROOMSAFE - Behavioral Grooming Detection Framework
- Detects early grooming patterns through behavioral analysis
- Works with anonymized conversation data and metadata
- Identifies progression stages, not isolated messages
- No explicit content processing

#### 🔒 HUMANSHIELD - Psychological Safety & Evidence Abstraction Layer
- Protects investigators, moderators, and analysts
- Prevents exposure to disturbing or traumatic material
- Abstracts sensitive evidence into safe representations
- Enforces exposure limits and cognitive shielding

---

## Purpose

This system is designed for:

- **Prevention**: Early detection of grooming behavioral patterns
- **Protection**: Shielding minors and potential victims
- **Safety**: Protecting investigators from psychological harm
- **Transparency**: Explainable and auditable decisions
- **Compliance**: Legal defensibility and accountability
- **Research**: Academic study and improvement of child safety measures

---

## Ethical Boundaries

### What This System IS

✅ A **risk signaling framework** for behavioral pattern detection
✅ A **preventive tool** focused on early intervention
✅ A **safety support system** with human-in-the-loop decision making
✅ A **research platform** for understanding grooming dynamics
✅ An **investigator protection mechanism** preventing trauma exposure

### What This System IS NOT

❌ A **surveillance system** for mass monitoring
❌ A **criminal accusation engine** that assigns guilt
❌ A **content filter** that processes explicit material
❌ An **autonomous decision-maker** without human oversight
❌ A **replacement** for law enforcement investigation

### Critical Principles

1. **Prevention over Reaction**: Focus on early behavioral signals
2. **Behavior over Content**: Analyze patterns, not message semantics
3. **Progression over Keywords**: Track stage development, not isolated terms
4. **Explainability over Black Box**: Every decision must be interpretable
5. **Human-in-the-Loop**: Critical decisions require human review
6. **Psychological Safety by Design**: Protect all participants
7. **Legal Auditability by Default**: Maintain comprehensive audit trails

---

## Architecture

### System Components

```
groomsafe/
├── core/
│   ├── data_models.py          # Pydantic data schemas
│   ├── feature_extraction.py   # Behavioral feature analysis
│   ├── progression_model.py    # Stage classification
│   ├── risk_scoring.py         # Risk assessment engine
│   ├── humanshield.py          # Psychological safety layer
│   ├── explainability.py       # Explanation generation
│   └── audit_log.py            # Audit trail management
├── api/
│   └── api.py                  # FastAPI REST endpoints
├── data/
│   └── synthetic/              # Synthetic test datasets
├── examples/
│   └── example_usage.py        # Usage demonstrations
└── tests/                      # Unit and integration tests
```

### Technology Stack

- **Python 3.8+**: Core implementation language
- **FastAPI**: REST API framework
- **Pydantic**: Data validation and schemas
- **NumPy**: Numerical computations
- **Uvicorn**: ASGI server

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone repository
git clone <repository-url>
cd GROOMSAFE

# Install dependencies
pip install -r requirements.txt

# Generate synthetic datasets (for testing)
cd groomsafe
python3 data/synthetic/generate_synthetic_data.py
```

---

## Usage

### Command-Line Example

```python
# Run example analysis
cd groomsafe
python3 examples/example_usage.py
```

### API Server

```bash
# Start FastAPI server
cd groomsafe/api
python3 api.py

# Server will run at http://localhost:8090
# API documentation at http://localhost:8090/docs
```

### Programmatic Usage

```python
from core.data_models import Conversation
from core.risk_scoring import RiskScoringEngine
from core.humanshield import HumanShieldLayer

# Load conversation
conversation = Conversation(...)

# Assess risk
risk_engine = RiskScoringEngine()
assessment = risk_engine.assess_risk(conversation)

# Create safe summary for analyst
humanshield = HumanShieldLayer()
safe_summary = humanshield.create_safe_summary(
    conversation,
    assessment,
    features,
    exposure_level="minimal"
)

print(f"Risk Score: {assessment.grooming_risk_score}/100")
print(f"Stage: {assessment.current_stage}")
```

---

## API Endpoints

### Core Endpoints

#### POST `/api/v1/assess`
Assess a conversation for grooming risk

**Request:**
```json
{
  "conversation": {
    "messages": [...],
    "start_time": "2024-01-01T00:00:00Z",
    "platform_type": "social_media",
    "is_synthetic": true
  },
  "exposure_level": "minimal",
  "analyst_id": "analyst_001"
}
```

**Response:**
```json
{
  "risk_assessment": {
    "grooming_risk_score": 75.3,
    "risk_level": "high",
    "current_stage": "isolation_attempts",
    "requires_human_review": true
  },
  "behavioral_features": {...},
  "humanshield_summary": {...},
  "explanation": {...}
}
```

#### GET `/health`
Health check endpoint

#### GET `/api/v1/audit/conversation/{conversation_id}`
Retrieve audit trail for a conversation

#### POST `/api/v1/analyst/check-safety`
Check analyst exposure limits

See full API documentation at `/docs` when server is running.

---

## Behavioral Features

The system analyzes **eight key behavioral features**:

1. **Contact Frequency Escalation**: Increasing message rate over time
2. **Persistence After Non-Response**: Continued messaging despite silence
3. **Time-of-Day Irregularity**: Messaging at unusual hours
4. **Emotional Dependency Indicators**: Patterns of emotional manipulation
5. **Isolation Pressure**: Attempts to separate target from others
6. **Secrecy Pressure**: Requests for privacy or confidentiality
7. **Platform Migration Attempts**: Efforts to move to other platforms
8. **Tone Shift Score**: Changes in linguistic patterns over time

All features are **abstract** and **non-explicit**, focusing on behavioral signals rather than content.

---

## Grooming Progression Stages

The system classifies conversations into five stages:

### 1. Initial Contact (Low Risk)
- Minimal behavioral signals
- Exploratory communication
- **Action**: Baseline monitoring

### 2. Trust Building (Moderate Risk)
- Increasing contact frequency
- Developing rapport
- **Action**: Enhanced monitoring

### 3. Emotional Dependency (High Risk)
- Emotional manipulation patterns
- Dependency building
- **Action**: Human review within 24 hours

### 4. Isolation Attempts (Critical Risk)
- Secrecy pressure
- Platform migration attempts
- **Action**: Urgent human review required

### 5. Escalation Risk (Critical Risk)
- Multiple high-risk signals
- Urgent intervention patterns
- **Action**: Immediate intervention required

---

## HUMANSHIELD Protection Features

### Analyst Safety Mechanisms

1. **Exposure Limits**
   - Maximum 20 cases per session
   - Maximum 5 high-risk cases per session
   - Maximum 2-hour session duration
   - Mandatory 15-minute breaks

2. **Content Abstraction**
   - No raw message content exposure
   - Clinical, neutral summaries only
   - Graph and timeline visualizations
   - Behavioral cluster classifications

3. **Exposure Tracking**
   - Per-analyst session monitoring
   - Cumulative exposure metrics
   - Automatic break enforcement
   - Safety status checks

---

## Explainability & Auditability

Every risk assessment includes:

- **Risk Score Breakdown**: Feature-by-feature contribution analysis
- **Stage Classification Rationale**: Why this stage was assigned
- **Confidence Metrics**: Assessment reliability indicators
- **Recommendations**: Specific action items based on risk level
- **Audit Trail**: Immutable log of all decisions
- **Limitation Disclosure**: Known system constraints

### Audit Logging

All system actions are logged with:
- Timestamp and actor identification
- Decision rationale
- Model version used
- Risk metrics
- Full metadata for compliance

---

## Legal Considerations

### Data Minimization
- System requires only **behavioral metadata**
- No storage of explicit content required
- Anonymization assumed at input
- Minimal data retention policies supported

### Human Review Requirements
- **High-risk assessments** require human review within 24 hours
- **Critical assessments** require immediate human review
- System provides decision support, not final verdicts
- All interventions must be approved by authorized personnel

### False Positive Handling
- System includes false positive reporting mechanism
- Feedback loop for continuous improvement
- Regular model validation recommended
- Threshold tuning based on operational data

### Compliance Readiness
- JSONL audit logs for external analysis
- Compliance report generation
- Exportable audit trails (JSON, CSV formats)
- Model versioning for reproducibility

---

## Research Applicability

This system is designed for:

- **Academic Research**: Understanding grooming behavioral dynamics
- **Safety Platform Development**: Integration into existing platforms
- **Policy Development**: Informing child safety regulations
- **Training Programs**: Educating investigators and moderators
- **Grant Applications**: Demonstrating technical feasibility
- **Publication**: Results suitable for peer-reviewed venues

### Validation Requirements

Before deployment:
1. Validate with domain experts (child safety professionals)
2. Test on diverse, representative datasets
3. Measure and report false positive/negative rates
4. Conduct bias and fairness analysis
5. Establish operational thresholds
6. Implement continuous monitoring

---

## Limitations

Users must understand:

- ⚠️ This is a **risk signaling system**, not proof of criminal activity
- ⚠️ **False positives are possible**; human judgment is essential
- ⚠️ System analyzes **behavior patterns**, not semantic content
- ⚠️ **Cultural context** may not be fully captured
- ⚠️ Effectiveness depends on **data quality and completeness**
- ⚠️ Regular **model updates** required for accuracy
- ⚠️ System is **one component** of comprehensive safety measures

---

## Non-Goals

This system explicitly **does not**:

- ❌ Process, generate, or store explicit sexual content
- ❌ Analyze images, audio, or video content
- ❌ Make autonomous decisions about interventions
- ❌ Replace law enforcement investigation
- ❌ Provide legal evidence without human validation
- ❌ Guarantee 100% accuracy in detection
- ❌ Work without human oversight

---

## Testing

### Synthetic Datasets

Four synthetic datasets are provided for testing:

1. **Low Risk**: Benign educational interaction
2. **Moderate Risk**: Concerning patterns, not critical
3. **High Risk**: Multiple risk factors, requires review
4. **Critical Risk**: Escalation risk, immediate action needed

### Running Tests

```bash
# Run example analysis on all datasets
cd groomsafe
python3 examples/example_usage.py

# Run unit tests (when implemented)
pytest tests/
```

---

## Future Enhancements

Planned improvements:

- [ ] Machine learning model integration (supervised learning on labeled data)
- [ ] Multi-language support
- [ ] Real-time streaming analysis
- [ ] Advanced visualization dashboard
- [ ] Integration with common platforms (Discord, etc.)
- [ ] Automated model retraining pipeline
- [ ] Enhanced bias detection and mitigation
- [ ] Cross-platform behavior correlation

---

## Contributing

This is a research and safety project. Contributions should:

- Maintain ethical boundaries
- Include comprehensive documentation
- Add unit tests for new features
- Preserve explainability and auditability
- Consider investigator safety
- Respect privacy and data minimization

---

## License

MIT License with Ethical Use Clause

Copyright (c) 2024 Joas Antonio

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

**Ethical Use Clause**: This software is intended solely for child safety, research, and educational purposes. Any use that harms, exploits, or endangers children or vulnerable populations is strictly prohibited.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## Author

**Joas Antonio**
- GitHub: [@CyberSecurityUP](https://github.com/CyberSecurityUP)
- Project: GROOMSAFE + HUMANSHIELD
- Focus: Cybersecurity, Child Safety, Behavioral Analysis

---

## Citation

If you use this system in research, please cite:

```bibtex
@software{groomsafe2024,
  author = {Antonio, Joas},
  title = {GROOMSAFE + HUMANSHIELD: Behavioral Grooming Prevention \& Investigator Protection Ecosystem},
  year = {2024},
  url = {https://github.com/CyberSecurityUP/GROOMSAFE}
}
```

---

## Contact & Support

For questions, issues, or research collaboration:

- **GitHub**: [CyberSecurityUP/GROOMSAFE](https://github.com/CyberSecurityUP)
- **Issues**: [GitHub Issues](https://github.com/CyberSecurityUP/GROOMSAFE/issues)
- **Author**: Joas Antonio - [@CyberSecurityUP](https://github.com/CyberSecurityUP)

---

## Disclaimer

This system is provided for **research, educational, and child safety purposes only**. It is designed as a **decision support tool** and should **never be used as the sole basis** for interventions affecting individuals. All deployments must include appropriate human oversight, legal review, and ethical safeguards.

The creators and contributors make no warranties about the accuracy, reliability, or completeness of this system. Users assume full responsibility for validation, deployment, and operational use.

---

## Acknowledgments

This system is built on research and best practices from:
- Child safety experts and organizations
- Platform trust and safety professionals
- Behavioral psychology research
- Machine learning fairness literature
- Investigator trauma prevention studies

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Status**: Research Prototype
