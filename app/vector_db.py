import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os
import uuid

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def create_collection(self, collection_name: str):
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def chunk_text(self, text: str, chunk_size: int = 512, chunk_overlap: int = 50) -> List[str]:
        """
        Simple text chunking without external dependencies
        """
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        
        for paragraph in paragraphs:
            words = paragraph.split()
            if len(words) <= chunk_size:
                # If paragraph is small enough, use as-is
                chunks.append(paragraph)
            else:
                # Split large paragraphs into smaller chunks
                current_chunk = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > chunk_size and current_chunk:
                        # Save current chunk
                        chunks.append(' '.join(current_chunk))
                        # Keep overlap for context
                        if chunk_overlap > 0:
                            current_chunk = current_chunk[-chunk_overlap:]
                            current_length = sum(len(w) + 1 for w in current_chunk)
                        else:
                            current_chunk = []
                            current_length = 0
                    
                    current_chunk.append(word)
                    current_length += len(word) + 1
                
                # Add the last chunk
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
        
        # Filter out empty chunks
        return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def add_documents(self, documents: List[Dict], collection_name: str = "qa_documents"):
        collection = self.create_collection(collection_name)
        
        ids = []
        embeddings = []
        metadatas = []
        documents_list = []
        
        for doc in documents:
            chunks = self.chunk_text(doc['content'])
            for i, chunk in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                embedding = self.embedder.encode(chunk).tolist()
                
                ids.append(chunk_id)
                embeddings.append(embedding)
                metadatas.append({
                    "source": doc['filename'],
                    "chunk_index": i
                })
                documents_list.append(chunk)
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents_list
        )
    
    def search(self, query: str, n_results: int = 5, collection_name: str = "qa_documents"):
        collection = self.create_collection(collection_name)
        query_embedding = self.embedder.encode(query).tolist()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results