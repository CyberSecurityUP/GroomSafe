# 🛡️ GROOMSAFE - Interface Gráfica Web

## ✨ NOVIDADE: Interface Gráfica Completa!

Agora o GROOMSAFE tem uma **interface web moderna** em inglês!

---

## 🚀 Como Abrir (SUPER FÁCIL)

### Opção 1: Um Clique
```bash
./OPEN_WEB.sh
```

### Opção 2: Manual
```bash
cd /opt/GROOMSAFE/groomsafe/api
python3 api.py
```

Depois abra no navegador:
```
http://localhost:8090
```

---

## 🎨 O Que Você Vai Ver

### Interface Moderna com:
- ✅ **Gauge animado** mostrando risco (0-100)
- ✅ **Cores intuitivas** (verde → amarelo → vermelho)
- ✅ **Gráficos visuais** de features comportamentais
- ✅ **Exemplos prontos** para testar
- ✅ **Construtor de mensagens** visual
- ✅ **Tudo em inglês** (padrão internacional)

### Painel Esquerdo - Entrada:
- Botões para carregar exemplos (Baixo, Moderado, Alto, Crítico)
- Construtor visual de mensagens (sem precisar JSON)
- Campo de entrada JSON (para usuários avançados)
- Configurações de plataforma e exposição

### Painel Direito - Resultados:
- **Círculo de risco** animado (tipo velocímetro)
- **Badge de nível** (Minimal, Low, Moderate, High, Critical)
- **Métricas**: Confiança, Estágio, Revisão Humana
- **Gráfico de features** (8 indicadores comportamentais)
- **HUMANSHIELD Summary** (proteção para analistas)
- **Recomendações** de ação
- **Features contribuindo** mais para o risco

---

## 🎯 Teste Rápido (30 segundos)

1. Abra http://localhost:8090
2. Clique no botão **"Critical Risk"** (vermelho)
3. Clique **"Analyze Conversation"**
4. Veja o resultado:
   - Risco: ~66/100
   - Nível: HIGH
   - Estágio: Isolation Attempts
   - Recomendação: Revisão humana necessária

---

## 📊 Níveis de Risco

| Score | Nível | Cor | Badge |
|-------|-------|-----|-------|
| 0-20 | Minimal | 🟢 Verde | Monitoramento básico |
| 21-40 | Low | 🔵 Azul | Monitoramento contínuo |
| 41-60 | Moderate | 🟡 Amarelo | Monitoramento aumentado |
| 61-80 | High | 🟠 Laranja | Revisão prioritária |
| 81-100 | Critical | 🔴 Vermelho | Intervenção imediata |

---

## 🎬 Como Usar

### Método 1: Exemplos Prontos (MAIS FÁCIL)
1. Clique em um dos 4 botões de exemplo
2. Veja a conversa carregada
3. Clique "Analyze Conversation"
4. Veja os resultados visuais

### Método 2: Construtor Visual
1. Selecione "Adult" ou "Minor"
2. Digite a mensagem
3. Clique "Add Message" (ou Enter)
4. Repita para criar conversa
5. Clique "Analyze"

### Método 3: JSON (Avançado)
1. Cole JSON no campo de texto
2. Clique "Analyze"

---

## 🌍 Tudo em Inglês

A interface está **totalmente em inglês** para:
- ✅ Padrão internacional
- ✅ Publicação científica
- ✅ Colaboração global
- ✅ Documentação unificada

**Termos principais:**
- **Risk Score** = Pontuação de Risco
- **Behavioral Features** = Features Comportamentais
- **Human Review** = Revisão Humana
- **Recommendations** = Recomendações

---

## 📱 Funciona Em

- ✅ Chrome / Edge
- ✅ Firefox
- ✅ Safari
- ✅ Mobile (celular/tablet)

---

## 🔗 Links Importantes

| O Que | URL |
|-------|-----|
| **Interface Web** | http://localhost:8090/ |
| Documentação API | http://localhost:8090/docs |
| Health Check | http://localhost:8090/health |

---

## 📚 Outras Formas de Usar

Prefere linha de comando? Veja:

```bash
# Demo rápido (4 exemplos)
python3 demo.py

# Análise detalhada
python3 direct_test.py

# Exemplos interativos
cd groomsafe && python3 examples/example_usage.py
```

---

## 🛑 Parar o Servidor

```bash
pkill -f "uvicorn api:app"
```

---

## 📖 Documentação Completa

- **Interface Web**: `WEB_INTERFACE.md` (inglês)
- **Início Rápido**: `START_WEB.md` (inglês)
- **Como Executar**: `HOW_TO_RUN.md` (inglês)
- **README**: `README.md` (inglês)
- **Executar CLI**: `EXECUTAR.md` (português)

---

## 🎉 Pronto!

Execute e veja a mágica:
```bash
./OPEN_WEB.sh
```

Ou acesse diretamente:
```
http://localhost:8090
```

**Divirta-se explorando a interface! 🚀**

---

## 💡 Dica

A interface web é a forma **mais fácil e visual** de usar o GROOMSAFE. Perfeita para:
- Demonstrações
- Testes rápidos
- Aprendizado
- Apresentações

Para automação e integração, use a API REST.
