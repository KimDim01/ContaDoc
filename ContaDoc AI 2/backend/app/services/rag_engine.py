from app.services.vector_store import vector_store
from app.services.hf_service import hf_client
from app.core.config import settings

class RAGEngine:
    def __init__(self):
        pass

    async def answer_question(self, client_id: str, question: str):
        # 1. Retrieve relevant documents from ChromaDB
        docs = vector_store.query_documents(client_id, question)

        # 2. Build the context for the LLM
        context = "\n\n".join([doc for doc in docs['documents'][0]])

        # 3. Professional Accounting Prompt
        system_prompt = (
            "You are a Senior Accounting AI Assistant for a prestigious firm. "
            "Your goal is to provide precise, accurate, and grounded answers based ONLY on the provided context. "
            "If the answer is not in the context, state that you don't have that information. "
            "Always cite the source document if available. Focus on numerical precision."
        )

        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {question}"

        # Use the Hugging Face Client instead of Claude
        answer = hf_client.chat_completion(full_prompt)

        return {
            "answer": answer,
            "sources": docs['metadatas'][0]
        }

rag_engine = RAGEngine()
