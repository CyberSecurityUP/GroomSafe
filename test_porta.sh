#!/bin/bash
# Teste rápido da porta 8090

echo "======================================"
echo "🧪 Testando GROOMSAFE API - Porta 8090"
echo "======================================"
echo ""

echo "1. Verificando se o servidor está rodando..."
if lsof -i :8090 > /dev/null 2>&1; then
    echo "   ✅ Servidor está rodando na porta 8090"
else
    echo "   ❌ Servidor NÃO está rodando na porta 8090"
    echo ""
    echo "Para iniciar:"
    echo "  cd /opt/GROOMSAFE/groomsafe/api"
    echo "  python3 api.py"
    exit 1
fi

echo ""
echo "2. Testando endpoint raiz (/)..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8090/ 2>/dev/null)
if [ "$STATUS" = "200" ]; then
    echo "   ✅ Endpoint / respondeu com 200 OK"
else
    echo "   ⚠️  Endpoint / respondeu com código: $STATUS"
fi

echo ""
echo "3. Testando health check..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8090/health 2>/dev/null)
if [ "$STATUS" = "200" ]; then
    echo "   ✅ Health check respondeu com 200 OK"
else
    echo "   ⚠️  Health check respondeu com código: $STATUS"
fi

echo ""
echo "======================================"
echo "✅ Testes concluídos!"
echo "======================================"
echo ""
echo "📖 Acesse a documentação em:"
echo "   http://localhost:8090/docs"
echo ""
