# 🌐 GROOMSAFE Web Interface

## Modern Graphical User Interface for Behavioral Risk Assessment

---

## 🚀 Quick Start

### Access the Interface

**Open in your browser:**
```
http://localhost:8090
```

The web interface will load automatically when you access the root URL.

### Alternative URLs

- **Web Interface**: http://localhost:8090/
- **API Docs**: http://localhost:8090/docs
- **API Root**: http://localhost:8090/api
- **Health Check**: http://localhost:8090/health

---

## ✨ Features

### 1. **Quick Load Examples**
- Pre-loaded synthetic conversations with different risk levels
- One-click testing with realistic scenarios
- Examples: Low, Moderate, High, and Critical risk

### 2. **Manual Input**
- JSON format conversation input
- Visual message builder (no JSON required)
- Customizable platform types
- Analyst exposure level control

### 3. **Real-Time Analysis**
- Live API communication
- Instant risk assessment
- Beautiful data visualization

### 4. **Comprehensive Results**
- Risk score with animated gauge (0-100)
- Risk level classification (Minimal → Critical)
- Confidence metrics
- Progression stage identification
- Behavioral feature breakdown
- HUMANSHIELD protection summary
- Actionable recommendations
- Feature contribution analysis

---

## 📖 How to Use

### Method 1: Quick Load (Fastest)

1. **Open** http://localhost:8090 in your browser
2. **Click** one of the example buttons:
   - 🟢 Low Risk - Educational conversation
   - 🟡 Moderate Risk - Concerning patterns
   - 🟠 High Risk - Multiple indicators
   - 🔴 Critical Risk - Escalation detected
3. **Click** "Analyze Conversation"
4. **View** instant results with risk score, features, and recommendations

### Method 2: Message Builder (Easy)

1. **Select** sender role (Adult/Minor)
2. **Type** message text
3. **Click** "Add Message" (or press Enter)
4. **Repeat** to build a conversation
5. **Click** "Analyze Conversation"

### Method 3: JSON Input (Advanced)

1. **Paste** JSON conversation data in the text area
2. **Format** (example below)
3. **Click** "Analyze Conversation"

**JSON Format:**
```json
[
  {
    "timestamp": "2024-01-01T10:00:00Z",
    "sender_role": "adult",
    "abstracted_text": "Hello, how are you?"
  },
  {
    "timestamp": "2024-01-01T10:05:00Z",
    "sender_role": "minor",
    "abstracted_text": "I'm fine, thanks."
  }
]
```

---

## 🎨 Interface Components

### Left Panel - Input

**Quick Load Examples**
- 4 pre-loaded scenarios
- Color-coded risk levels
- One-click loading

**Manual Input**
- Platform type selector
- JSON text area
- Visual message builder
- Exposure level control
- Optional analyst ID

### Right Panel - Results

**Risk Assessment Card**
- Animated circular progress gauge
- Risk score (0-100)
- Risk level badge
- Confidence percentage
- Current stage
- Human review requirement

**Behavioral Features Chart**
- 8 behavioral indicators
- Visual progress bars
- Percentage values
- Color-coded risk levels

**HUMANSHIELD Protection Summary**
- Behavioral cluster classification
- Temporal pattern analysis
- Key risk indicators list
- Analyst-safe abstractions

**Recommendations**
- Actionable next steps
- Risk-appropriate guidance
- Human review triggers

**Feature Contributions**
- Top contributing factors
- Feature values
- Contribution weights
- Explanatory descriptions

---

## 🎯 Understanding Results

### Risk Scores

| Score Range | Risk Level | Color | Meaning |
|-------------|------------|-------|---------|
| 0-20 | Minimal | 🟢 Green | Low risk, baseline monitoring |
| 21-40 | Low | 🔵 Blue | Slight concern, continued monitoring |
| 41-60 | Moderate | 🟡 Yellow | Increased monitoring recommended |
| 61-80 | High | 🟠 Orange | High-priority review required |
| 81-100 | Critical | 🔴 Red | Immediate intervention needed |

### Progression Stages

1. **Initial Contact** - First interactions, exploratory
2. **Trust Building** - Developing rapport
3. **Emotional Dependency** - Manipulation patterns
4. **Isolation Attempts** - Secrecy and isolation
5. **Escalation Risk** - Critical intervention required

### Behavioral Features

- **Contact Frequency**: Message rate escalation
- **Persistence**: Continued messaging despite non-response
- **Time Irregularity**: Off-hours messaging
- **Emotional Dependency**: Manipulation indicators
- **Isolation Pressure**: Separation attempts
- **Secrecy Pressure**: Privacy requests
- **Platform Migration**: Moving to other platforms
- **Tone Shift**: Linguistic changes

---

## 🔧 Configuration

### Platform Types
- Social Media
- Messaging App
- Gaming Platform
- Educational Forum
- Other

### Exposure Levels
- **Minimal** (Default) - Basic abstractions only
- **Moderate** - More detail with safeguards
- **Detailed** - Maximum context with protection

### Analyst ID
- Optional identifier for tracking
- Enables exposure limit enforcement
- Required for session management

---

## 🛡️ Safety Features

### HUMANSHIELD Protection
- No raw content exposure
- Clinical, neutral summaries
- Visual abstractions (graphs, timelines)
- Exposure limits enforced
- Mandatory break recommendations

### Audit Trail
- All assessments logged
- Timestamp tracking
- Model version recording
- Decision rationale captured

---

## 🚨 Troubleshooting

### API Status Indicator

**Green Dot** = API Online ✅
**Red Dot** = API Offline ❌

### Common Issues

**Problem**: "API is offline"
**Solution**:
```bash
cd /opt/GROOMSAFE/groomsafe/api
python3 api.py
```

**Problem**: Page not loading
**Solution**: Check server is running on port 8090:
```bash
lsof -i :8090
```

**Problem**: Example buttons not working
**Solution**: Ensure synthetic datasets exist:
```bash
ls groomsafe/data/synthetic/
```

**Problem**: Analysis fails
**Solution**: Check browser console (F12) for errors

---

## 💻 Technical Details

### Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: FastAPI (Python)
- **Communication**: REST API (JSON)
- **Styling**: Modern CSS with animations
- **Responsive**: Mobile-friendly design

### API Endpoints Used
- `GET /health` - Server status
- `POST /api/v1/assess` - Risk assessment
- `GET /api/v1/stage/description/{stage}` - Stage info

### Data Flow
1. User inputs conversation
2. Frontend validates and formats
3. POST request to API
4. Backend analyzes with GROOMSAFE
5. Response with assessment
6. Frontend visualizes results

---

## 🎬 Demo Workflow

1. **Open** http://localhost:8090
2. **Click** "Critical Risk" example
3. **See** conversation loaded (17 messages)
4. **Click** "Analyze Conversation"
5. **Watch** risk score animate to ~66/100
6. **View** "High Risk" classification
7. **Read** "Isolation Attempts" stage
8. **Check** behavioral features (all elevated)
9. **Review** HUMANSHIELD summary (safe abstractions)
10. **Read** recommendations (human review required)

---

## 📱 Mobile Access

The interface is **fully responsive** and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

---

## 🔗 Quick Links

- **Web Interface**: http://localhost:8090/
- **API Documentation**: http://localhost:8090/docs
- **Health Check**: http://localhost:8090/health
- **GitHub**: [Repository URL]
- **Documentation**: ../README.md

---

## ⚙️ Advanced Usage

### Keyboard Shortcuts
- `Enter` in message builder = Add message
- Browser refresh = Reset form

### Browser DevTools
- Press `F12` to open console
- View network requests
- Debug issues
- Monitor API calls

### Customization
- Edit `style.css` for styling changes
- Modify `app.js` for behavior changes
- Update `index.html` for structure changes

---

## 📊 Features Comparison

| Feature | Web Interface | API Docs | CLI |
|---------|---------------|----------|-----|
| Visual Results | ✅ | ❌ | ❌ |
| Easy Input | ✅ | ⚠️ | ❌ |
| Real-time Feedback | ✅ | ⚠️ | ✅ |
| Example Loading | ✅ | ❌ | ⚠️ |
| Batch Processing | ❌ | ✅ | ✅ |
| Scripting | ❌ | ✅ | ✅ |

---

## 🎓 Best Practices

1. **Start with examples** to understand the system
2. **Use message builder** for quick testing
3. **Monitor API status** indicator
4. **Review all tabs** in results panel
5. **Export data** via API if needed
6. **Follow recommendations** for high-risk cases

---

## 📝 Notes

- Interface is **English-only** for international consistency
- All data is **processed locally** (no external services)
- Assessments are **logged** for audit trail
- Interface uses **synthetic data** for examples
- **No real conversations** should be used without proper authorization

---

## ✅ Checklist

Before using the interface:
- [ ] Server running on port 8090
- [ ] Browser supports modern JavaScript
- [ ] Example datasets generated
- [ ] API status shows green
- [ ] Network allows localhost connections

---

**Version**: 1.0.0
**Last Updated**: December 2024
**License**: MIT with Ethical Use Clause

For issues or questions, see main documentation or API docs.
