# 🎯 GROOMSAFE - Complete Usage Guide

## Choose Your Method

### 🌐 Option 1: Web Interface (RECOMMENDED) ⭐

**Best for:** Visual analysis, quick testing, demonstrations

```bash
# Just run this
./OPEN_WEB.sh

# Or manually
cd /opt/GROOMSAFE/groomsafe/api
python3 api.py

# Then open browser
http://localhost:8090
```

**Features:**
- ✅ Beautiful modern interface
- ✅ No coding required
- ✅ Real-time visualizations
- ✅ One-click examples
- ✅ Animated risk scores
- ✅ Mobile-friendly

**See:** `START_WEB.md` and `WEB_INTERFACE.md`

---

### 🖥️ Option 2: Command Line Demo

**Best for:** Quick testing, seeing all examples

```bash
cd /opt/GROOMSAFE
python3 demo.py
```

**Output:**
- Analyzes 4 conversations
- Shows risk scores
- Displays stages
- Shows confidence levels

---

### 🔬 Option 3: Detailed Analysis

**Best for:** Understanding the system

```bash
cd /opt/GROOMSAFE
python3 direct_test.py
```

**Output:**
- Complete feature breakdown
- HUMANSHIELD summary
- Top contributing factors
- Recommendations

---

### 📚 Option 4: Interactive Examples

**Best for:** Step-by-step learning

```bash
cd /opt/GROOMSAFE/groomsafe
python3 examples/example_usage.py
```

**Features:**
- Analyzes all 4 risk levels
- Press Enter between examples
- Detailed explanations
- Full audit trail

---

### 🔌 Option 5: API Direct

**Best for:** Integration, automation

```bash
# 1. Start server
cd /opt/GROOMSAFE/groomsafe/api
python3 api.py

# 2. Use API docs
http://localhost:8090/docs

# 3. Or use curl
curl -X POST "http://localhost:8090/api/v1/assess" \
  -H "Content-Type: application/json" \
  -d @groomsafe/data/synthetic/high_risk_conversation.json
```

---

### 🐍 Option 6: Python Script

**Best for:** Custom analysis, research

```python
import json
import sys
sys.path.insert(0, "groomsafe")

from core.data_models import Conversation
from core.risk_scoring import RiskScoringEngine

# Load conversation
with open("groomsafe/data/synthetic/high_risk_conversation.json") as f:
    conv = Conversation(**json.load(f))

# Analyze
engine = RiskScoringEngine()
result = engine.assess_risk(conv)

# Results
print(f"Risk: {result.grooming_risk_score:.1f}/100")
print(f"Level: {result.risk_level.value.upper()}")
print(f"Stage: {result.current_stage.value}")
```

---

## Quick Comparison

| Method | Ease | Visual | Speed | Detail |
|--------|------|--------|-------|--------|
| Web Interface | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| CLI Demo | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Direct Test | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Examples | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| API | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Python | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## What Each Tool Does

### 🌐 Web Interface
- Visual risk assessment
- Interactive charts
- Real-time API communication
- Example loading
- Message builder

### 📊 demo.py
- Quick overview of all risk levels
- Compare 4 conversations
- Summary statistics

### 🔍 direct_test.py
- Detailed single analysis
- Feature breakdown
- HUMANSHIELD summary
- Recommendations

### 📖 example_usage.py
- Step-by-step walkthrough
- Interactive (press Enter)
- Educational

### 🔌 API
- REST interface
- JSON input/output
- Integration ready
- Swagger docs

### 🐍 Python
- Programmatic access
- Full control
- Custom workflows

---

## Recommended Learning Path

1. **Start with Web Interface** (http://localhost:8090)
   - Load "Low Risk" example
   - Click "Analyze"
   - Explore results

2. **Try CLI Demo** (`python3 demo.py`)
   - See all risk levels
   - Compare scores

3. **Run Detailed Test** (`python3 direct_test.py`)
   - Understand features
   - See HUMANSHIELD

4. **Explore API Docs** (http://localhost:8090/docs)
   - Try endpoints
   - See JSON structure

5. **Write Custom Code**
   - Use Python examples
   - Build integrations

---

## Files Overview

```
/opt/GROOMSAFE/
├── OPEN_WEB.sh          ← Run this to open web interface!
├── START_WEB.md         ← Web interface quick start
├── WEB_INTERFACE.md     ← Web interface full docs
├── HOW_TO_RUN.md        ← This file
├── demo.py              ← Quick CLI demo
├── direct_test.py       ← Detailed analysis
├── README.md            ← Full documentation
├── QUICKSTART.md        ← General quick start
│
└── groomsafe/
    ├── web/             ← Web interface files
    │   ├── index.html
    │   ├── style.css
    │   └── app.js
    ├── api/             ← API server
    │   └── api.py
    ├── core/            ← Core modules
    ├── data/synthetic/  ← Example datasets
    └── examples/        ← Usage examples
```

---

## Port Information

- **Web Interface**: Port 8090
- **API**: Port 8090 (same server)
- **Changed from**: 8080 → 8090 (less common port)

---

## Quick Commands Cheat Sheet

```bash
# Open web interface
./OPEN_WEB.sh

# OR manually start server
cd groomsafe/api && python3 api.py

# Quick demo (all examples)
python3 demo.py

# Detailed test
python3 direct_test.py

# Interactive examples
cd groomsafe && python3 examples/example_usage.py

# Check if running
lsof -i :8090

# Stop server
pkill -f "uvicorn api:app"

# View logs
tail -f groomsafe/logs/*.jsonl
```

---

## URLs Reference

| What | URL |
|------|-----|
| **Web Interface** | http://localhost:8090/ |
| API Docs (Swagger) | http://localhost:8090/docs |
| API Docs (ReDoc) | http://localhost:8090/redoc |
| API Root | http://localhost:8090/api |
| Health Check | http://localhost:8090/health |

---

## Need Help?

- **Web Interface**: See `WEB_INTERFACE.md`
- **API**: See `README.md` or http://localhost:8090/docs
- **Examples**: See `QUICKSTART.md`
- **Portuguese**: See `EXECUTAR.md`

---

## Best Choice for You

- **Just want to try it?** → Web Interface (`./OPEN_WEB.sh`)
- **Need quick results?** → CLI Demo (`python3 demo.py`)
- **Want to learn?** → Examples (`python3 examples/example_usage.py`)
- **Building integration?** → API Docs (http://localhost:8090/docs)
- **Research/Development?** → Python scripts

---

**Recommendation:** Start with the **Web Interface** - it's the easiest and most visually appealing way to explore GROOMSAFE!

```bash
./OPEN_WEB.sh
```

Then visit: **http://localhost:8090** 🚀
