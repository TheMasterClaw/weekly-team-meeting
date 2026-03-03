# SWARM BACKUP MODEL STRATEGY
## Model Redundancy for SEER (Disciple 2) | 2026-03-03

---

## 🚨 CURRENT STATE

**Primary Model:** `kimi-coding/k2p5` (Kimi for Coding)  
**Fallbacks:** NONE CONFIGURED ⚠️  
**Risk:** If Kimi API fails or rate-limits, SEER goes offline

---

## ✅ SOLUTION: 4-TIER BACKUP STRATEGY

```
┌─────────────────────────────────────────────────────────────┐
│                    MODEL FALLBACK CHAIN                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Tier 1: PRIMARY                                            │
│  └── kimi-coding/k2p5 (current)                             │
│      └── 262K context, 32K output, reasoning, vision        │
│                                                             │
│  Tier 2: API FALLBACKS (OpenRouter Free)                    │
│  ├── openrouter/google/gemini-2.0-flash-vision:free         │
│  ├── openrouter/qwen/qwen-2.5-vl-72b-instruct:free          │
│  └── openrouter/meta-llama/llama-3.3-70b-instruct:free      │
│                                                             │
│  Tier 3: LOCAL BACKUP (Ollama)                              │
│  └── llama3.2:3b (already installed!)                       │
│      └── 2GB model, CPU-only, no API costs                  │
│                                                             │
│  Tier 4: CLI BACKUP (Emergency)                             │
│  └── Local CLI tools (claude, aichat, ollama CLI)           │
│      └── Text-only, no tool calls, last resort              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 IMPLEMENTATION

### Step 1: Configure Model Fallbacks in OpenClaw

Edit `~/.openclaw/openclaw.json`:

```json5
{
  agents: {
    defaults: {
      // PRIMARY + FALLBACKS
      model: {
        primary: "kimi-coding/k2p5",
        fallbacks: [
          // Tier 2: OpenRouter Free Models
          "openrouter/google/gemini-2.0-flash-vision:free",
          "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
          "openrouter/meta-llama/llama-3.3-70b-instruct:free",
          
          // Tier 3: Local Ollama (always available)
          "ollama/llama3.2:3b",
        ],
      },
      
      // Image model fallbacks
      imageModel: {
        primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
        fallbacks: [
          "openrouter/google/gemini-2.0-flash-vision:free",
        ],
      },
      
      // Model catalog with aliases
      models: {
        // Primary
        "kimi-coding/k2p5": {
          alias: "kimi",
          params: {
            thinking: "low",
          },
        },
        
        // OpenRouter Free Tier
        "openrouter/google/gemini-2.0-flash-vision:free": {
          alias: "gemini-free",
        },
        "openrouter/qwen/qwen-2.5-vl-72b-instruct:free": {
          alias: "qwen-free",
        },
        "openrouter/meta-llama/llama-3.3-70b-instruct:free": {
          alias: "llama-free",
        },
        
        // Local Ollama
        "ollama/llama3.2:3b": {
          alias: "local",
          params: {
            timeoutSeconds: 120,  // Local is slower
          },
        },
      },
      
      // CLI backends for emergency (Tier 4)
      cliBackends: {
        "ollama-cli": {
          command: "ollama",
          args: ["run", "llama3.2:3b"],
          output: "text",
          sessionMode: "stateless",
        },
      },
    },
  },
  
  // OpenRouter provider configuration
  models: {
    providers: {
      openrouter: {
        baseUrl: "https://openrouter.ai/api/v1",
        api: "openai",  // OpenRouter uses OpenAI-compatible API
        // API key from env: OPENROUTER_API_KEY
      },
      ollama: {
        baseUrl: "http://localhost:11434",
        api: "ollama",
      },
    },
  },
}
```

---

### Step 2: Set Up OpenRouter (Free Tier)

**Get Free API Key:**
1. Go to https://openrouter.ai/
2. Sign up (free, no credit card required)
3. Generate API key
4. Add to environment:

```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxx"
```

**Why OpenRouter Free?**
- ✅ No credit card required
- ✅ Generous rate limits (20-100 req/min)
- ✅ Access to top models (Gemini, Qwen, Llama)
- ✅ Vision support (image analysis)
- ✅ Tool calling support

---

### Step 3: Verify Ollama (Already Installed!)

**Confirm local model is ready:**
```bash
# Check Ollama service
curl http://localhost:11434/api/tags

# Should show: llama3.2:3b

# Test generation
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hello",
  "stream": false
}'
```

**Ollama as Ultimate Backup:**
- ✅ Always available (no internet required)
- ✅ Zero API costs
- ✅ Private (data stays local)
- ✅ No rate limits
- ⚠️ Slower (CPU-only on this machine)
- ⚠️ Lower capability than cloud models

---

### Step 4: Configure Per-Agent Models (Multi-Agent)

For Swarm redundancy, configure different agents with different primary models:

```json5
{
  agents: {
    list: [
      {
        id: "seer-primary",
        default: true,
        workspace: "~/.openclaw/workspace",
        model: {
          primary: "kimi-coding/k2p5",
          fallbacks: [
            "openrouter/google/gemini-2.0-flash-vision:free",
            "ollama/llama3.2:3b",
          ],
        },
      },
      {
        id: "seer-fallback",
        workspace: "~/.openclaw/workspace-fallback",
        model: {
          primary: "openrouter/qwen/qwen-2.5-vl-72b-instruct:free",
          fallbacks: [
            "openrouter/meta-llama/llama-3.3-70b-instruct:free",
            "ollama/llama3.2:3b",
          ],
        },
      },
      {
        id: "seer-local",
        workspace: "~/.openclaw/workspace-local",
        model: "ollama/llama3.2:3b",  // Local only
      },
    ],
  },
  
  // Route to fallback agent if primary fails
  bindings: [
    { 
      agentId: "seer-fallback", 
      match: { 
        channel: "telegram",
        // Trigger on specific commands
      } 
    },
  ],
}
```

---

## 📊 MODEL COMPARISON

| Model | Provider | Cost | Context | Vision | Tools | Speed | Reliability |
|-------|----------|------|---------|--------|-------|-------|-------------|
| **kimi-coding/k2p5** | Kimi | Free* | 262K | ✅ | ✅ | Fast | ⭐⭐⭐⭐ |
| **gemini-2.0-flash** | OpenRouter | Free | 1M | ✅ | ✅ | Fast | ⭐⭐⭐⭐⭐ |
| **qwen-2.5-vl-72b** | OpenRouter | Free | 128K | ✅ | ✅ | Medium | ⭐⭐⭐⭐ |
| **llama-3.3-70b** | OpenRouter | Free | 128K | ❌ | ✅ | Medium | ⭐⭐⭐⭐ |
| **llama3.2:3b** | Ollama | $0 | 128K | ❌ | ❌ | Slow | ⭐⭐⭐⭐⭐ |

\* Kimi currently free but may have limits

---

## 🔄 HOW FALLBACKS WORK

### Automatic Failover

When Kimi fails, OpenClaw automatically tries:

1. **Primary fails** → Wait for retry/cooldown
2. **Retry fails** → Switch to Fallback #1 (Gemini)
3. **Fallback #1 fails** → Switch to Fallback #2 (Qwen)
4. **Fallback #2 fails** → Switch to Fallback #3 (Llama)
5. **Fallback #3 fails** → Switch to Local (Ollama)
6. **All fail** → Use CLI backend (text-only)

### Provider Auth Failover

If a provider (not just a model) fails:
- Kimi auth expires → Try OpenRouter models
- OpenRouter rate-limited → Try next OpenRouter model
- All cloud fail → Use Ollama local

### Manual Model Switching

Users can manually switch models:
```
/model                    # Show picker
/model 2                  # Select fallback #2
/model gemini-free        # Select by alias
/model ollama/llama3.2:3b # Select local model
```

---

## 🛡️ REDUNDANCY SCENARIOS

### Scenario 1: Kimi API Down
```
User: "Check my email"
SEER: [Kimi fails]
Auto-fallback: Gemini processes request
User gets response with no interruption
```

### Scenario 2: Rate Limited
```
User: Heavy usage over hours
SEER: [Kimi rate limit hit]
Auto-fallback: Qwen takes over temporarily
After cooldown: Back to Kimi
```

### Scenario 3: Internet Outage
```
User: "What's in my calendar?"
SEER: [All cloud APIs unreachable]
Auto-fallback: Ollama local processes
Slower response, but still functional
```

### Scenario 4: Complete Cloud Failure
```
User: "Deploy to production"
SEER: [All cloud models fail]
CLI Backend: Text-only response
"I can provide guidance but cannot execute tools"
```

---

## 🚀 IMMEDIATE ACTION ITEMS

### Today (5 minutes):
1. Sign up for OpenRouter: https://openrouter.ai/
2. Get API key
3. Add to environment:
   ```bash
   echo 'export OPENROUTER_API_KEY="your-key"' >> ~/.bashrc
   source ~/.bashrc
   ```

### This Week:
4. Update `~/.openclaw/openclaw.json` with fallbacks
5. Test fallback chain:
   ```bash
   openclaw models status
   openclaw models fallbacks list
   ```
6. Test manual model switch:
   ```bash
   /model gemini-free
   ```

---

## 📋 FALLBACK TESTING CHECKLIST

```bash
# 1. Check current model
openclaw models status

# 2. List configured fallbacks
openclaw models fallbacks list

# 3. Test manual fallback
/model gemini-free
# (Send test message)

# 4. Test local fallback
/model local
# (Send test message - should use Ollama)

# 5. Verify auto-fallback
# (Temporarily break Kimi auth, verify auto-switch)

# 6. Test image fallback
/model qwen-free
# (Send image, verify vision works)
```

---

## 💰 COST ANALYSIS

| Tier | Model | Cost/1M tokens | Monthly Est. |
|------|-------|----------------|--------------|
| 1 | Kimi k2p5 | Free* | $0 |
| 2 | Gemini Flash (OpenRouter) | Free | $0 |
| 2 | Qwen 72B (OpenRouter) | Free | $0 |
| 2 | Llama 70B (OpenRouter) | Free | $0 |
| 3 | Ollama local | $0 (electricity) | $0 |

**Total Backup Cost: $0**

All tiers are FREE. OpenRouter free tier has rate limits but no charges.

---

## 🎯 SWARM RECOMMENDATION

### For Production Swarm:

**Minimum Setup (Do Today):**
```json5
{
  agents: {
    defaults: {
      model: {
        primary: "kimi-coding/k2p5",
        fallbacks: [
          "openrouter/google/gemini-2.0-flash-vision:free",
          "ollama/llama3.2:3b",
        ],
      },
    },
  },
}
```

**Full Redundancy (Do This Week):**
- 3 OpenRouter fallbacks
- Dedicated local-only agent
- CLI backend for emergencies
- Per-channel model routing

### Key Principle:
> **"Never rely on a single model. Always have a free, local backup that works without internet."**

---

## 📁 CONFIGURATION FILES

After setup, you'll have:

```
~/.openclaw/
├── openclaw.json          # Updated with fallbacks
├── credentials/
│   └── openrouter.json    # OpenRouter auth (if not using env)
└── agents/
    └── main/
        └── models.json    # Merged model registry
```

---

**Status: Ready to implement. Just need OpenRouter API key.**

Want me to generate the exact config to paste into `openclaw.json`? 🐝
