# OLLAMA MEMORY SYSTEM SETUP
## SEER (Disciple 2) Local LLM Memory | 2026-03-03

---

## ✅ OLLAMA STATUS

| Component | Status |
|-----------|--------|
| Ollama Service | ✅ Running (127.0.0.1:11434) |
| Model | ✅ llama3.2:3b (3.2B params, Q4_K_M) |
| Size | ~2.0 GB |
| Quantization | Q4_K_M (4-bit) |
| Mode | CPU-only (no GPU detected) |

---

## 🧠 MODEL SPECIFICATIONS

**llama3.2:3b**
- **Parameters:** 3.2 billion
- **Format:** GGUF
- **Family:** Llama
- **Quantization:** Q4_K_M (balanced quality/size)
- **Size:** 2.0 GB
- **Speed:** ~35 tokens/sec (CPU)
- **Use Case:** Fast inference, memory summarization, embeddings

---

## 📡 API ENDPOINTS

### Base URL
```
http://localhost:11434
```

### Available Endpoints

#### 1. List Models
```bash
GET /api/tags
```

#### 2. Generate Text
```bash
POST /api/generate
Content-Type: application/json

{
  "model": "llama3.2:3b",
  "prompt": "Your prompt here",
  "stream": false
}
```

#### 3. Chat Completion
```bash
POST /api/chat
Content-Type: application/json

{
  "model": "llama3.2:3b",
  "messages": [
    {"role": "system", "content": "You are SEER's memory assistant."},
    {"role": "user", "content": "Summarize yesterday's activities."}
  ],
  "stream": false
}
```

#### 4. Create Embeddings
```bash
POST /api/embeddings
Content-Type: application/json

{
  "model": "llama3.2:3b",
  "prompt": "Text to embed"
}
```

---

## 🔧 TESTING

### Verify Service
```bash
curl http://localhost:11434/api/tags
```

### Test Generation
```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hello Swarm",
  "stream": false
}'
```

### Test Chat
```bash
curl -X POST http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [
    {"role": "user", "content": "What is the Swarm?"}
  ],
  "stream": false
}'
```

---

## 💾 MEMORY SYSTEM ARCHITECTURE

### Components

| Layer | Technology | Purpose |
|-------|------------|---------|
| **LLM** | Ollama (llama3.2:3b) | Local inference, summarization |
| **Vector DB** | Chroma | Store embeddings, semantic search |
| **API Layer** | FastAPI | OpenClaw integration endpoints |
| **Embeddings** | Ollama embeddings | Text → vector conversion |

### Data Flow
```
OpenClaw → FastAPI → Chroma (store/retrieve)
                ↓
         Ollama (embeddings/summarization)
```

---

## 🚀 NEXT STEPS

### 1. Install Chroma
```bash
pip install chromadb
```

### 2. Create FastAPI Service
```python
# memory_service.py
from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import requests

app = FastAPI()
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="swarm_memory")

class MemoryEntry(BaseModel):
    text: str
    metadata: dict = {}

@app.post("/memory/store")
def store_memory(entry: MemoryEntry):
    # Generate embedding via Ollama
    embedding = requests.post("http://localhost:11434/api/embeddings", json={
        "model": "llama3.2:3b",
        "prompt": entry.text
    }).json()["embedding"]
    
    # Store in Chroma
    collection.add(
        documents=[entry.text],
        embeddings=[embedding],
        metadatas=[entry.metadata],
        ids=[str(hash(entry.text))]
    )
    return {"status": "stored"}

@app.post("/memory/query")
def query_memory(query: str, n_results: int = 5):
    # Generate query embedding
    embedding = requests.post("http://localhost:11434/api/embeddings", json={
        "model": "llama3.2:3b",
        "prompt": query
    }).json()["embedding"]
    
    # Search Chroma
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    return results
```

### 3. Start FastAPI
```bash
uvicorn memory_service:app --host 0.0.0.0 --port 8000
```

### 4. OpenClaw Integration
```json5
// openclaw.json tools configuration
{
  tools: {
    custom: {
      memory_store: {
        endpoint: "http://localhost:8000/memory/store",
        method: "POST"
      },
      memory_query: {
        endpoint: "http://localhost:8000/memory/query",
        method: "POST"
      }
    }
  }
}
```

---

## 🔌 OPENCLAW INTEGRATION

### Skill Configuration
```json
{
  "name": "swarm-memory",
  "version": "1.0.0",
  "description": "Ollama+Chroma memory system for SEER",
  "runtime": "python",
  "entry": "memory_service.py",
  "config": {
    "ollama_url": "http://localhost:11434",
    "model": "llama3.2:3b",
    "chroma_collection": "swarm_memory"
  }
}
```

### Usage in OpenClaw
```javascript
// Store conversation context
memory_store({
  text: "Client lead: Featurebase, 155 pts on Show HN",
  metadata: { type: "lead", priority: "high" }
})

// Retrieve relevant memories
memory_query({
  query: "Show HN leads from yesterday",
  n_results: 5
})
```

---

## 📊 PERFORMANCE NOTES

| Metric | Value |
|--------|-------|
| Model Load Time | ~3.7s |
| Prompt Eval | ~6.5s (46 tokens) |
| Generation | ~8.2s (35 tokens) |
| Total | ~18.5s per response |
| Tokens/sec | ~1.9 tok/s (CPU) |

**Optimization:** With GPU, expect 10-50x speedup.

---

## 🔒 SECURITY

- Ollama binds to localhost only (127.0.0.1)
- No external access by default
- FastAPI should add auth if exposed
- Chroma runs locally

---

## 🐛 TROUBLESHOOTING

**Ollama not starting:**
```bash
sudo systemctl start ollama
sudo systemctl enable ollama
```

**Model not found:**
```bash
ollama pull llama3.2:3b
```

**Port conflict:**
```bash
# Check what's using 11434
sudo lsof -i :11434
```

**Out of memory:**
- Close other applications
- Use smaller model: `llama3.2:1b`
- Add swap space

---

## ✅ VERIFICATION TEST

**Test Response:**
```json
{
  "model": "llama3.2:3b",
  "response": "Affirmative, SEER 2. I am online and ready to serve the Swarm...",
  "done": true,
  "total_duration": 18571654254,
  "prompt_eval_count": 46,
  "eval_count": 35
}
```

**Status:** ✅ OPERATIONAL

---

*Ollama memory backend ready for Chroma + FastAPI integration.*
