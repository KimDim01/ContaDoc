import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings

class VectorStore:
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)

    def get_or_create_collection(self, client_id: str):
        """
        Each client gets their own collection to ensure strict data isolation.
        """
        collection_name = f"client_{client_id}"
        return self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, client_id: str, chunks, metadatas, ids):
        """
        Adds processed chunks to the client's specific vector collection.
        """
        collection = self.get_or_create_collection(client_id)
        collection.add(
            documents=[doc.page_content for doc in chunks],
            metadatas=metadatas,
            ids=ids
        )

    def query_documents(self, client_id: str, query: str, n_results: int = 5):
        """
        Searches for the most relevant chunks for a given query.
        """
        collection = self.get_or_create_collection(client_id)
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

vector_store = VectorStore()
