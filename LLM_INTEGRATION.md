# 🤖 LLM-Enhanced Analysis - GROOMSAFE

## Overview

GROOMSAFE now supports **LLM-enhanced analysis** to enrich behavioral grooming detection with AI-powered insights. This feature adds contextual understanding to complement the existing behavioral pattern analysis.

## Supported LLM Providers

### 1. **Ollama** (Default - Local & Free) ⭐ RECOMMENDED
- **Advantages**:
  - Free and open-source
  - Runs locally (privacy-first)
  - No API keys required
  - No cost per request
- **Requirements**: Ollama installed locally
- **Installation**: [https://ollama.ai](https://ollama.ai)
- **Recommended Models**:
  - `llama-guard-3` - Meta's safety moderation model (Best for grooming detection)
  - `llama3.2` - General purpose, good reasoning
  - `mistral` - Fast and accurate
  - `gemma2` - Google's safety-focused model

### 2. **Google Gemini**
- Requires API key
- Models: `gemini-1.5-pro`, `gemini-1.5-flash`
- Get API key: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 3. **Anthropic Claude**
- Requires API key
- Models: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- Get API key: [https://console.anthropic.com/](https://console.anthropic.com/)

### 4. **OpenAI ChatGPT**
- Requires API key
- Models: `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`
- Get API key: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

## Installation & Setup

### Option 1: Ollama (Recommended)

1. **Install Ollama**:
   ```bash
   # macOS
   brew install ollama

   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh

   # Windows
   # Download from https://ollama.ai/download
   ```

2. **Start Ollama**:
   ```bash
   ollama serve
   ```

3. **Pull Recommended Model**:
   ```bash
   ollama pull llama-guard-3
   ```

4. **Verify Installation**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

### Option 2: Cloud Providers

Simply obtain an API key from your chosen provider and enter it in the web interface.

## Usage

### Web Interface

1. **Navigate to GROOMSAFE**: [http://localhost:8090](http://localhost:8090)

2. **Expand LLM Configuration**:
   - Click on "🤖 LLM-Enhanced Analysis (Optional)"

3. **Configure**:
   - ✅ Check "Enable LLM Analysis"
   - Select Provider (default: Ollama)
   - Select Model
   - Enter API Key (if using cloud provider)

4. **Test Connection**:
   - Click "Test Connection"
   - Verify status shows "✓ Connected"

5. **Run Analysis**:
   - Submit your conversation
   - View AI-enhanced insights in results

### API Usage

```python
import requests

# Example with Ollama
response = requests.post('http://localhost:8090/api/v1/assess', json={
    "conversation": {
        "messages": [...],
        "platform_type": "messaging_app"
    },
    "llm_enabled": True,
    "llm_provider": "ollama",
    "llm_model": "llama-guard-3"
})

# Example with Gemini
response = requests.post('http://localhost:8090/api/v1/assess', json={
    "conversation": {
        "messages": [...],
        "platform_type": "messaging_app"
    },
    "llm_enabled": True,
    "llm_provider": "gemini",
    "llm_model": "gemini-1.5-pro",
    "llm_api_key": "YOUR_GEMINI_API_KEY"
})

result = response.json()
llm_analysis = result['risk_assessment']['llm_analysis']
```

### Check LLM Status

```bash
# Check if Ollama is available
curl "http://localhost:8090/api/v1/llm/status?provider=ollama&model=llama-guard-3"

# Get recommended models
curl "http://localhost:8090/api/v1/llm/models"
```

## LLM Analysis Output

The LLM analysis provides:

```json
{
    "provider": "ollama",
    "model": "llama-guard-3",
    "severity_assessment": "high",
    "confidence": 0.85,
    "risk_factors": [
        "Secrecy requests detected",
        "Emotional manipulation patterns",
        "Attempts to isolate target"
    ],
    "grooming_indicators": [
        "Trust exploitation",
        "Boundary testing",
        "Platform migration attempts"
    ],
    "explanation": "The conversation shows multiple concerning behaviors...",
    "recommended_actions": [
        "Flag for immediate human review",
        "Document all exchanges",
        "Consider escalating to authorities"
    ]
}
```

## Key Features

### 1. **Multilingual Support**
- LLM analyzes conversations in English, Portuguese, and Spanish
- Detects grooming patterns across languages

### 2. **Context-Aware**
- Understands nuanced manipulation tactics
- Identifies implicit threats and coercion

### 3. **Complementary Analysis**
- Works alongside behavioral feature extraction
- Provides additional confidence layer

### 4. **Privacy-First**
- Ollama runs 100% locally
- No data sent to external servers
- Full control over your infrastructure

## Performance Considerations

### Ollama (Local)
- **Latency**: 2-10 seconds (depending on model size)
- **Cost**: $0 (free)
- **Privacy**: 100% local
- **Requires**: 8GB+ RAM for llama-guard-3

### Cloud Providers
- **Latency**: 1-5 seconds
- **Cost**: Per-token pricing
- **Privacy**: Data sent to provider
- **Requires**: Internet connection + API key

## Best Practices

1. **Use Ollama for Production**:
   - Better privacy compliance
   - No ongoing costs
   - Predictable performance

2. **Choose Right Model**:
   - `llama-guard-3`: Safety/moderation tasks ⭐
   - `llama3.2`: General grooming detection
   - `mistral`: When speed is critical
   - `gemma2`: Google ecosystem integration

3. **Combine with Behavioral Analysis**:
   - Don't rely solely on LLM
   - Use as complementary evidence
   - Trust behavioral patterns for primary detection

4. **Monitor Performance**:
   - Track analysis time
   - Review LLM confidence scores
   - Validate against known cases

## Troubleshooting

### "LLM not available"

**For Ollama**:
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Check API
curl http://localhost:11434/api/tags
```

### "Model not found"

```bash
# Pull the model
ollama pull llama-guard-3

# List available models
ollama list
```

### "Connection timeout"

- Increase timeout in LLM config
- Check firewall settings
- Verify Ollama endpoint: `http://localhost:11434`

## Security Considerations

### Data Privacy
- **Ollama**: All processing local, no external requests
- **Cloud APIs**: Data transmitted to provider servers

### API Key Storage
- Never commit API keys to version control
- Use environment variables
- Consider secrets management tools

### Content Filtering
- LLM sees abstracted text only
- No explicit content in prompts
- HUMANSHIELD protection still applies

## Advanced Configuration

### Custom Prompts

Modify `/opt/GROOMSAFE/groomsafe/core/llm_analyzer.py`:

```python
def _build_prompt(self, messages: List[Dict[str, Any]]) -> str:
    # Customize your prompt here
    prompt = f"""Your custom analysis instructions..."""
    return prompt
```

### Model Parameters

Adjust temperature and tokens in `LLMConfig`:

```python
config = LLMConfig(
    provider="ollama",
    model="llama-guard-3",
    temperature=0.3,  # Lower = more consistent
    max_tokens=1000   # Adjust for longer responses
)
```

## Roadmap

- [ ] Fine-tuned models for grooming detection
- [ ] Batch analysis support
- [ ] Caching for repeated patterns
- [ ] Multi-model ensemble voting
- [ ] Custom model training pipelines

## Resources

- **Ollama**: https://ollama.ai
- **Llama Guard**: https://huggingface.co/meta-llama/Llama-Guard-3-8B
- **GROOMSAFE Docs**: `/opt/GROOMSAFE/README.md`

## Support

For issues or questions:
1. Check Ollama logs: `ollama logs`
2. Test API endpoint: `curl http://localhost:8090/api/v1/llm/status`
3. Review server logs: Check uvicorn output

---

**Version**: 1.0.0
**Last Updated**: December 2024
**License**: MIT with Ethical Use Clause
