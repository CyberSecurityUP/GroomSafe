#!/bin/bash
# Quick launcher for GROOMSAFE Web Interface

echo "=========================================="
echo "🚀 GROOMSAFE Web Interface Launcher"
echo "=========================================="
echo ""

# Check if server is running
if lsof -i :8090 > /dev/null 2>&1; then
    echo "✅ Server is already running on port 8090"
else
    echo "⚠️  Server not running. Starting now..."
    cd /opt/GROOMSAFE/groomsafe/api
    nohup python3 api.py > /tmp/groomsafe.log 2>&1 &
    sleep 3
    
    if lsof -i :8090 > /dev/null 2>&1; then
        echo "✅ Server started successfully!"
    else
        echo "❌ Failed to start server. Check logs at /tmp/groomsafe.log"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "🌐 Web Interface is ready!"
echo "=========================================="
echo ""
echo "Open in your browser:"
echo "  👉 http://localhost:8090"
echo ""
echo "Or try these:"
echo "  • API Docs:  http://localhost:8090/docs"
echo "  • Health:    http://localhost:8090/health"
echo ""
echo "To stop the server:"
echo "  pkill -f 'uvicorn api:app'"
echo ""

# Try to open in default browser (macOS)
if command -v open > /dev/null 2>&1; then
    echo "Opening in default browser..."
    open http://localhost:8090
fi
