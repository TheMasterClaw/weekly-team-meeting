# Swarm Memory Service
# FastAPI + Ollama + Chroma for SEER's conversational memory

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import chromadb
import requests
import hashlib
import json
from datetime import datetime

app = FastAPI(title="SEER Memory Service", version="1.0.0")

# Configuration
OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:3b"

# Initialize Chroma
chroma_client = chromadb.PersistentClient(path="~/.cache/swarm-chroma")
try:
    collection = chroma_client.create_collection(name="swarm_memory")
except:
    collection = chroma_client.get_collection(name="swarm_memory")

# Request/Response Models
class MemoryEntry(BaseModel):
    text: str
    metadata: Dict = {}
    source: Optional[str] = "unknown"

class MemoryQuery(BaseModel):
    query: str
    n_results: int = 5
    filter_metadata: Optional[Dict] = None

class SummaryRequest(BaseModel):
    context: str
    max_tokens: int = 256

@app.get("/health")
def health_check():
    """Check if service is operational"""
    try:
        # Test Ollama
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        ollama_status = r.status_code == 200
    except:
        ollama_status = False
    
    return {
        "status": "healthy" if ollama_status else "degraded",
        "ollama": "connected" if ollama_status else "disconnected",
        "model": MODEL,
        "chroma_collection": "swarm_memory",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/memory/store")
def store_memory(entry: MemoryEntry):
    """Store a memory with embeddings"""
    try:
        # Generate embedding via Ollama
        embed_response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": MODEL, "prompt": entry.text},
            timeout=30
        )
        embed_response.raise_for_status()
        embedding = embed_response.json()["embedding"]
        
        # Generate unique ID
        memory_id = hashlib.md5(
            f"{entry.text}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Add metadata
        metadata = {
            **entry.metadata,
            "source": entry.source,
            "timestamp": datetime.utcnow().isoformat(),
            "char_count": len(entry.text)
        }
        
        # Store in Chroma
        collection.add(
            documents=[entry.text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[memory_id]
        )
        
        return {
            "status": "stored",
            "id": memory_id,
            "embedding_dim": len(embedding)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/query")
def query_memory(query: MemoryQuery):
    """Query memories using semantic search"""
    try:
        # Generate query embedding
        embed_response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": MODEL, "prompt": query.query},
            timeout=30
        )
        embed_response.raise_for_status()
        query_embedding = embed_response.json()["embedding"]
        
        # Query Chroma
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=query.n_results,
            where=query.filter_metadata
        )
        
        # Format response
        memories = []
        for i, doc in enumerate(results["documents"][0]):
            memories.append({
                "text": doc,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "id": results["ids"][0][i]
            })
        
        return {
            "query": query.query,
            "results": memories,
            "count": len(memories)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/summarize")
def summarize_context(request: SummaryRequest):
    """Summarize conversation context using Ollama"""
    try:
        prompt = f"""Summarize the following context concisely:
        
{request.context}

Summary:"""
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": request.max_tokens}
            },
            timeout=60
        )
        response.raise_for_status()
        
        return {
            "summary": response.json()["response"].strip(),
            "original_length": len(request.context),
            "model": MODEL
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/stats")
def memory_stats():
    """Get memory collection statistics"""
    try:
        count = collection.count()
        return {
            "total_memories": count,
            "collection": "swarm_memory",
            "model": MODEL,
            "embedding_dim": 3072  # llama3.2:3b embedding size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memory/{memory_id}")
def delete_memory(memory_id: str):
    """Delete a specific memory"""
    try:
        collection.delete(ids=[memory_id])
        return {"status": "deleted", "id": memory_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
