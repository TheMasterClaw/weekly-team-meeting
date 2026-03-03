# QMD SWARM INTEGRATION SETUP
## Daily 04:20 Index Configuration | 2026-03-03

---

## ✅ QMD INSTALLED & CONFIGURED

### Installation
```bash
npm install -g @tobilu/qmd
```
**Status:** ✅ Complete (259 packages installed)

---

## 📚 COLLECTIONS CREATED

| Collection | Path | Files | Purpose |
|------------|------|-------|---------|
| **swarm-intel** | `/intel/*.md` | 7 | Intelligence reports, recon data, audits |
| **swarm-memory** | `/memory/*.md` | 1 | Daily memory logs, operational records |
| **swarm-tools** | `/tools/**/README.md` | 51 | Tool documentation, capability references |

**Total:** 59 documents indexed

---

## 🧠 CONTEXT ADDED

| Collection | Context Description |
|------------|---------------------|
| swarm-intel | "Swarm intelligence reports, reconnaissance data, security audits, and competitive analysis" |
| swarm-memory | "Swarm daily memory logs and operational records" |
| swarm-tools | "Swarm tool documentation, README files, and capability references" |

---

## ⏰ CRON JOB: 04:20 DAILY INDEX

**Job ID:** `a0ae7fd6-c31d-4a73-95f1-0d2b3dedf6eb`

**Schedule:**
- **Time:** 04:20 UTC daily
- **Expression:** `20 4 * * *`
- **Timezone:** UTC

**Command:**
```bash
qmd update --pull && qmd embed
```

**Behavior:**
- Runs in isolated session (doesn't pollute main chat)
- Announces completion to last active channel
- Updates all collections and regenerates embeddings

**Next Run:** 2026-03-04 at 04:20 UTC

---

## 🔍 HOW TO USE QMD

### Search Commands
```bash
# Full-text search (fast)
qmd search "devops leads"

# Vector semantic search
qmd vsearch "infrastructure automation"

# Hybrid search (best quality)
qmd query "client acquisition strategy"

# Search specific collection
qmd search "oracle cloud" -c swarm-intel

# JSON output for agents
qmd query "bounty platforms" --json

# Export files list
qmd search "competitive intel" --all --files
```

### Get Documents
```bash
# Get by path
qmd get intel/recon_report_2026-03-03.md

# Get by docid (from search results)
qmd get "#abc123"

# Multi-get by pattern
qmd multi-get "intel/*.md" --json
```

### Maintenance
```bash
# Check status
qmd status

# Manual update
qmd update

# Force re-embed
qmd embed -f

# Cleanup cache
qmd cleanup
```

---

## 🔌 MCP SERVER (For Agent Integration)

**Start MCP server:**
```bash
# HTTP mode (persistent)
qmd mcp --http --daemon

# Check status
qmd status

# Stop
qmd mcp stop
```

**Tools available:**
- `qmd_search` - BM25 keyword search
- `qmd_vector_search` - Semantic search
- `qmd_deep_search` - Hybrid + re-ranking
- `qmd_get` - Retrieve document
- `qmd_multi_get` - Batch retrieve
- `qmd_status` - Index health

---

## 📊 INDEX DETAILS

**Storage:** `~/.cache/qmd/index.sqlite`

**Models (auto-downloaded):**
- embeddinggemma-300M-Q8_0 (~300MB) - Vector embeddings
- qwen3-reranker-0.6b-q8_0 (~640MB) - Re-ranking
- qmd-query-expansion-1.7B-q4_k_m (~1.1GB) - Query expansion

**Search Pipeline:**
1. Query Expansion (LLM generates variations)
2. BM25 Full-text search
3. Vector semantic search
4. RRF Fusion (Reciprocal Rank Fusion)
5. LLM Re-ranking
6. Position-aware blending

---

## 🎯 SWARM USE CASES

### 1. Lead Research
```bash
qmd query "indie hackers devops" --json -n 10
```
Find previous research on specific lead types.

### 2. Competitive Intel
```bash
qmd search "pricing strategy" -c swarm-intel
```
Recall competitive analysis documents.

### 3. Tool Lookup
```bash
qmd vsearch "browser automation"
```
Find tools by capability description.

### 4. Memory Retrieval
```bash
qmd get memory/2026-03-03.md
```
Access daily operational logs.

### 5. Cross-Reference
```bash
qmd multi-get "intel/*report*.md" --json | jq '.[].title'
```
List all report titles.

---

## ⚠️ EMBED STATUS

**Initial embed:** Running in background (session: warm-daisy)
- Downloads 3 GGUF models (~2GB total)
- Generates embeddings for 59 documents
- May take 5-15 minutes on first run

**Subsequent embeds:** Faster (incremental updates)

---

## 🔧 TROUBLESHOOTING

**If QMD not found:**
```bash
export PATH="$PATH:$(npm bin -g)"
# or
npx @tobilu/qmd <command>
```

**If embed fails:**
```bash
# Check disk space
df -h ~/.cache/qmd

# Clean and retry
qmd cleanup
qmd embed -f
```

**If models won't download:**
```bash
# Manual download check
ls -la ~/.cache/qmd/models/
```

---

## 📈 NEXT STEPS

1. ✅ QMD installed
2. ✅ Collections configured
3. ✅ Context added
4. ✅ Cron job scheduled (04:20 daily)
5. ⏳ Initial embed completing
6. ⏳ MCP server for agent integration (optional)

---

*QMD integration complete. Swarm knowledge base searchable at 04:20 daily.*
