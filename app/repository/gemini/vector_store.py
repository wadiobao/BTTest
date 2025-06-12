import os
import logging
import uuid
from typing import List, Optional
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, db_path: str, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedding_function = HuggingFaceEmbeddings(model_name=embedding_model)
        
        # Khởi tạo ChromaDB client
        db_client = chromadb.PersistentClient(path=db_path)
        self.vectorstore = Chroma(
            client=db_client,
            collection_name="child_chunks_for_search",
            embedding_function=self.embedding_function,
        )
    
    async def store_child_chunks(self, child_chunks: List[Document]) -> None:
        """
        Lưu các child chunks vào vector store.
        """
        if child_chunks:
            child_ids = [str(uuid.uuid4()) for _ in child_chunks]
            await self.vectorstore.aadd_documents(
                documents=child_chunks, 
                ids=child_ids
            )
            logger.info(f"Đã thêm {len(child_chunks)} child chunks vào ChromaDB")
    
    async def search(
        self, 
        query: str, 
        k: int = 5,
        source_document: Optional[str] = None
    ) -> List[Document]:
        """
        Tìm kiếm các documents tương tự.
        """
        search_kwargs = {'k': k}
        
        if source_document:
            search_kwargs['filter'] = {"source": source_document}
            logger.info(f"Tìm kiếm trong source: {source_document}")
        
        return await self.vectorstore.asimilarity_search(
            query,
            **search_kwargs
        )
    
    def get_all_sources(self) -> List[str]:
        """
        Lấy danh sách tất cả các sources trong database.
        """
        collection = self.vectorstore._collection
        results = collection.get()
        if results and results['metadatas']:
            return list(set(
                metadata['source'] 
                for metadata in results['metadatas'] 
                if 'source' in metadata
            ))
        return [] 