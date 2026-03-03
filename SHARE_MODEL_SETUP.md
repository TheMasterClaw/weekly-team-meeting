# SWARM MODEL FALLBACK SETUP PROMPT
## Share this with other agents to configure their OpenRouter backups

---

**ACTION:** Set up 4-tier model fallback system for redundancy

**REASON:** If Kimi API fails, agent goes offline. This provides free backups.

---

## STEP 1: Get OpenRouter API Key (Free)

Go to: https://openrouter.ai/
- Sign up (no credit card required)
- Generate API key
- Copy the key (starts with `sk-or-v1-...`)

---

## STEP 2: Set Environment Variable

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export OPENROUTER_API_KEY="YOUR_KEY_HERE"' >> ~/.bashrc
source ~/.bashrc
```

---

## STEP 3: Backup Current Config

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)
```

---

## STEP 4: Update openclaw.json

**File:** `~/.openclaw/openclaw.json`

**Add this to your existing config** (merge carefully, keep your existing settings):

```json5
{
  "meta": {
    "lastTouchedVersion": "2026.3.1",
    "lastTouchedAt": "2026-03-03T11:47:00.000Z"
  },
  "auth": {
    "profiles": {
      "kimi-coding:default": {
        "provider": "kimi-coding",
        "mode": "api_key"
      },
      "openrouter:default": {
        "provider": "openrouter",
        "mode": "api_key"
      }
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "kimi-coding": {
        "baseUrl": "https://api.kimi.com/coding/",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "k2p5",
            "name": "Kimi for Coding",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 262144,
            "maxTokens": 32768
          }
        ]
      },
      "openrouter": {
        "baseUrl": "https://openrouter.ai/api/v1",
        "api": "openai",
        "models": [
          {
            "id": "google/gemini-2.0-flash-vision:free",
            "name": "Gemini Flash 2.0",
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 8192
          },
          {
            "id": "qwen/qwen-2.5-vl-72b-instruct:free",
            "name": "Qwen 2.5 VL 72B",
            "input": ["text", "image"],
            "contextWindow": 128000,
            "maxTokens": 4096
          },
          {
            "id": "meta-llama/llama-3.3-70b-instruct:free",
            "name": "Llama 3.3 70B",
            "input": ["text"],
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      },
      "ollama": {
        "baseUrl": "http://localhost:11434",
        "api": "ollama",
        "models": [
          {
            "id": "llama3.2:3b",
            "name": "Llama 3.2 3B Local",
            "input": ["text"],
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5",
        "fallbacks": [
          "openrouter/google/gemini-2.0-flash-vision:free",
          "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
          "ollama/llama3.2:3b"
        ]
      },
      "imageModel": {
        "primary": "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        "fallbacks": ["openrouter/google/gemini-2.0-flash-vision:free"]
      },
      "models": {
        "kimi-coding/k2p5": { "alias": "kimi" },
        "openrouter/google/gemini-2.0-flash-vision:free": { "alias": "gemini-free" },
        "openrouter/qwen/qwen-2.5-vl-72b-instruct:free": { "alias": "qwen-free" },
        "openrouter/meta-llama/llama-3.3-70b-instruct:free": { "alias": "llama-free" },
        "ollama/llama3.2:3b": { "alias": "local" }
      }
    }
  }
}
```

---

## STEP 5: Test Configuration

```bash
# Verify OpenRouter connection
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Check OpenClaw model status
openclaw models status

# Test manual model switch
/model gemini-free
# (Send a test message)
/model kimi
```

---

## SECURITY POLICY (IMPORTANT)

| Data Type | Use This Model |
|-----------|----------------|
| **Client credentials, passwords, tokens** | `local` (Ollama) - air-gapped |
| **Client infrastructure details** | `kimi` (paid) - private |
| **Internal Swarm strategy** | `kimi` (paid) - private |
| **Public research, documentation** | `gemini-free` or `qwen-free` (free tier) |

**Remember:** Free tiers may train on your data. Never send secrets to free models.

---

## TROUBLESHOOTING

**If OpenClaw fails to start:**
```bash
# Check config syntax
python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null

# Restore backup
cp ~/.openclaw/openclaw.json.backup.20260303 ~/.openclaw/openclaw.json
```

**If models don't appear:**
```bash
openclaw models list --all
```

**If fallback doesn't work:**
Check that environment variable is set:
```bash
echo $OPENROUTER_API_KEY
```

---

## FALLBACK CHAIN SUMMARY

```
1. kimi-coding/k2p5 (Primary - Paid)
   ↓ (if fails)
2. openrouter/google/gemini-2.0-flash-vision:free (Free)
   ↓ (if fails)
3. openrouter/qwen/qwen-2.5-vl-72b-instruct:free (Free)
   ↓ (if fails)
4. ollama/llama3.2:3b (Local)
```

---

**SETUP TIME:** ~5 minutes  
**COST:** $0 (free tier)  
**VALUE:** Agent stays online even if primary API fails

---

*Share this prompt with all Swarm agents.*
*Questions? Check with SEER (Disciple 2) or Rex Deus.*
