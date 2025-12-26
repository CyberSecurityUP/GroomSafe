#!/usr/bin/env python3
"""
GROOMSAFE - Demonstração Rápida
Analisa as 4 conversas de exemplo
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, "groomsafe")

from core.data_models import Conversation
from core.risk_scoring import RiskScoringEngine

datasets = [
    ("BAIXO RISCO", "low_risk_conversation.json", "Interação educacional normal"),
    ("RISCO MODERADO", "moderate_risk_conversation.json", "Alguns padrões preocupantes"),
    ("ALTO RISCO", "high_risk_conversation.json", "Múltiplos indicadores de risco"),
    ("RISCO CRÍTICO", "critical_risk_conversation.json", "Escalação crítica - ação urgente"),
]

engine = RiskScoringEngine()

print("=" * 80)
print("🛡️  GROOMSAFE - DEMONSTRAÇÃO DE ANÁLISE DE RISCO")
print("=" * 80)
print()

for nome, arquivo, descricao in datasets:
    caminho = Path(f"groomsafe/data/synthetic/{arquivo}")

    with open(caminho) as f:
        conversa = Conversation(**json.load(f))

    avaliacao = engine.assess_risk(conversa)

    print(f"{'─' * 80}")
    print(f"📊 {nome}")
    print(f"{'─' * 80}")
    print(f"Descrição: {descricao}")
    print(f"Mensagens: {len(conversa.messages)}")
    print()
    print(f"  Pontuação de Risco:  {avaliacao.grooming_risk_score:>6.1f}/100")
    print(f"  Nível:               {avaliacao.risk_level.value.upper():>12}")
    print(f"  Confiança:           {avaliacao.confidence_level:>11.1%}")
    print(f"  Estágio:             {avaliacao.current_stage.value.replace('_', ' ').title()}")
    print(f"  Revisão Humana:      {'SIM ⚠️ ' if avaliacao.requires_human_review else 'Não'}")
    print()

print("=" * 80)
print("✅ Análise Completa!")
print("=" * 80)
print()
print("📖 Para mais detalhes, execute:")
print("   python3 direct_test.py          # Teste detalhado")
print("   python3 examples/example_usage.py  # Exemplos completos")
print()
print("🌐 API Server: http://localhost:8090/docs")
print()
