# 🚀 GROOMSAFE Web Interface - Quick Start

## How to Access

1. **Make sure the server is running:**
   ```bash
   cd /opt/GROOMSAFE/groomsafe/api
   python3 api.py
   ```

2. **Open in your browser:**
   ```
   http://localhost:8090
   ```

3. **You're done!** The interface will load automatically.

---

## Quick Test (30 seconds)

1. Click the **"Critical Risk"** button (red badge)
2. Click **"Analyze Conversation"**
3. Watch the risk score animate to ~66/100
4. See the results with:
   - Risk level: HIGH
   - Stage: Isolation Attempts
   - Features: All elevated
   - Recommendations: Human review required

---

## What You'll See

### Beautiful Modern Interface
- Clean, professional design
- Real-time API status indicator
- Animated risk score gauge
- Color-coded risk levels
- Interactive charts and graphs

### Two Main Panels

**Left Panel - Input:**
- Quick load examples (4 scenarios)
- Message builder (no coding needed)
- JSON input (for advanced users)
- Platform and exposure settings

**Right Panel - Results:**
- Circular risk score (0-100)
- Risk level badge
- Behavioral features chart
- HUMANSHIELD protection summary
- Recommendations list
- Feature contributions

---

## All in English 🌍

The entire interface is in English for international standardization:
- Interface labels
- Descriptions
- Results
- Recommendations
- Error messages

---

## Features

✅ One-click example loading
✅ Visual message builder
✅ Real-time analysis
✅ Animated results
✅ Risk score gauge (0-100)
✅ 8 behavioral features
✅ HUMANSHIELD protection
✅ Actionable recommendations
✅ Mobile responsive
✅ No installation needed (just browser)

---

## URLs

| What | URL |
|------|-----|
| **Web Interface** | http://localhost:8090/ |
| API Documentation | http://localhost:8090/docs |
| API Root | http://localhost:8090/api |
| Health Check | http://localhost:8090/health |

---

## Browser Support

✅ Chrome / Chromium
✅ Firefox
✅ Safari
✅ Edge
✅ Mobile browsers

---

## Quick Commands

```bash
# Start server
cd /opt/GROOMSAFE/groomsafe/api
python3 api.py

# Check if running
lsof -i :8090

# Stop server
pkill -f "uvicorn api:app"

# View logs
tail -f groomsafe/logs/*.jsonl
```

---

## That's It!

Just open **http://localhost:8090** and you're ready to go! 🎉

For detailed documentation, see `WEB_INTERFACE.md`
