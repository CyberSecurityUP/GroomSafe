# 🚀 Como Executar o GROOMSAFE

## Opção 1: Teste Rápido (Recomendado)

```bash
cd /opt/GROOMSAFE
python3 direct_test.py
```

**O que faz**: Analisa uma conversa de alto risco e mostra todos os resultados.

---

## Opção 2: Ver Todos os Exemplos

```bash
cd /opt/GROOMSAFE/groomsafe
python3 examples/example_usage.py
```

**O que faz**: Analisa 4 conversas diferentes (pressione Enter para avançar entre elas).

---

## Opção 3: API no Navegador

O servidor estará rodando! Abra no navegador:

```
http://localhost:8090/docs
```

**O que faz**: Interface interativa para testar a API.

---

## Opção 4: Analisar Conversa Específica

### Risco Baixo:
```bash
cd /opt/GROOMSAFE
python3 -c "
import json, sys
sys.path.insert(0, 'groomsafe')
from core.data_models import Conversation
from core.risk_scoring import RiskScoringEngine

with open('groomsafe/data/synthetic/low_risk_conversation.json') as f:
    conv = Conversation(**json.load(f))

result = RiskScoringEngine().assess_risk(conv)
print(f'Risco: {result.grooming_risk_score:.1f}/100 - {result.risk_level.value.upper()}')
print(f'Estágio: {result.current_stage.value}')
"
```

### Risco Crítico:
```bash
cd /opt/GROOMSAFE
python3 -c "
import json, sys
sys.path.insert(0, 'groomsafe')
from core.data_models import Conversation
from core.risk_scoring import RiskScoringEngine

with open('groomsafe/data/synthetic/critical_risk_conversation.json') as f:
    conv = Conversation(**json.load(f))

result = RiskScoringEngine().assess_risk(conv)
print(f'Risco: {result.grooming_risk_score:.1f}/100 - {result.risk_level.value.upper()}')
print(f'Estágio: {result.current_stage.value}')
print(f'Revisão Humana Necessária: {result.requires_human_review}')
"
```

---

## 📊 Datasets Disponíveis

| Arquivo | Nível de Risco |
|---------|----------------|
| `low_risk_conversation.json` | Baixo |
| `moderate_risk_conversation.json` | Moderado |
| `high_risk_conversation.json` | Alto |
| `critical_risk_conversation.json` | Crítico |

Todos em: `groomsafe/data/synthetic/`

---

## 🛑 Parar o Servidor

O servidor API está rodando em background. Para parar:

```bash
pkill -f "uvicorn api:app"
```

Para reiniciar:

```bash
cd /opt/GROOMSAFE/groomsafe/api
python3 api.py
```

---

## ✅ Teste Agora

Execute este comando para ver funcionar:

```bash
python3 direct_test.py
```
