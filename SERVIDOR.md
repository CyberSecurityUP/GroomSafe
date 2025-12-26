# 🌐 Servidor GROOMSAFE API

## ✅ Servidor Ativo

**Porta**: 8090
**Status**: ✅ Rodando
**URL Base**: http://localhost:8090

---

## 📖 Acessar Documentação

### Documentação Interativa (Swagger UI)
```
http://localhost:8090/docs
```
Interface completa para testar todos os endpoints.

### Documentação Alternativa (ReDoc)
```
http://localhost:8090/redoc
```
Documentação em formato alternativo.

### Health Check
```
http://localhost:8090/health
```
Verificar status do servidor.

---

## 🔧 Controlar o Servidor

### Verificar se está rodando
```bash
ps aux | grep uvicorn
```

### Parar o servidor
```bash
pkill -f "uvicorn api:app"
```

### Iniciar o servidor
```bash
cd /opt/GROOMSAFE/groomsafe/api
python3 api.py
```

Ou diretamente com uvicorn:
```bash
cd /opt/GROOMSAFE/groomsafe/api
uvicorn api:app --host 0.0.0.0 --port 8090 --reload
```

---

## 🧪 Testar API

### Teste Rápido via Curl
```bash
# Health check
curl http://localhost:8090/health

# Informações básicas
curl http://localhost:8090/

# Descrição de um estágio
curl http://localhost:8090/api/v1/stage/description/emotional_dependency
```

### Teste com Python
```python
import requests

# Health check
response = requests.get("http://localhost:8090/health")
print(response.json())
```

---

## 📡 Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Informações básicas |
| `/health` | GET | Status do servidor |
| `/docs` | GET | Documentação Swagger |
| `/api/v1/assess` | POST | Avaliar conversa |
| `/api/v1/stage/description/{stage}` | GET | Descrição do estágio |
| `/api/v1/analyst/check-safety` | POST | Verificar segurança do analista |
| `/api/v1/audit/conversation/{id}` | GET | Trilha de auditoria |

---

## 🚀 Exemplo de Uso

```bash
# Avaliar uma conversa de risco moderado
curl -X POST "http://localhost:8090/api/v1/assess" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": {
      "messages": [...],
      "start_time": "2024-01-01T00:00:00Z"
    },
    "exposure_level": "minimal"
  }'
```

---

## 📝 Notas

- **Porta 8090** escolhida para evitar conflitos com portas comuns
- **Auto-reload** ativado: mudanças no código reiniciam automaticamente
- **CORS** habilitado para desenvolvimento
- **Logs** salvos em `groomsafe/logs/`

---

## 🔗 Links Rápidos

- **Docs**: http://localhost:8090/docs
- **Health**: http://localhost:8090/health
- **ReDoc**: http://localhost:8090/redoc
