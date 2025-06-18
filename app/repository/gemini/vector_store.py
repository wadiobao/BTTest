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
        Lưu các child chunks vào vector store theo từng lô để tránh lỗi max batch size.
        """
        if not child_chunks:
            logger.info("Không có child chunks nào để lưu.")
            return

        # Định nghĩa kích thước lô an toàn
        BATCH_SIZE = 2000
        
        logger.info(f"Tổng số chunks cần lưu: {len(child_chunks)}. Bắt đầu xử lý theo lô với kích thước {BATCH_SIZE}.")

        # Tạo trước tất cả các ID
        all_ids = [str(uuid.uuid4()) for _ in child_chunks]

        # Vòng lặp để xử lý và thêm từng lô
        for i in range(0, len(child_chunks), BATCH_SIZE):
            # Lấy ra lô hiện tại của cả documents và IDs
            batch_docs = child_chunks[i:i + BATCH_SIZE]
            batch_ids = all_ids[i:i + BATCH_SIZE]
            
            logger.info(f"Đang lưu lô từ chunk thứ {i} đến {i + len(batch_docs)}...")
            
            # Gọi lệnh aadd_documents cho chỉ lô hiện tại
            await self.vectorstore.aadd_documents(
                documents=batch_docs, 
                ids=batch_ids
            )
            
            logger.info(f"Lưu lô thành công.")

        logger.info(f"Đã thêm thành công tất cả {len(child_chunks)} child chunks vào ChromaDB.")
    
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

    async def get_all_documents(self, source_document: Optional[str] = None) -> List[Document]:
        """
        Lấy tất cả documents từ vector store.
        
        Args:
            source_document: Tài liệu nguồn cụ thể (nếu có)
            
        Returns:
            List[Document]: Danh sách tất cả documents
        """
        collection = self.vectorstore._collection
        where = {"source": source_document} if source_document else None
        results = collection.get(where=where)
        
        if not results or not results['documents']:
            return []
            
        documents = []
        for i in range(len(results['documents'])):
            doc = Document(
                page_content=results['documents'][i],
                metadata=results['metadatas'][i] if results['metadatas'] else {}
            )
            documents.append(doc)
            
        return documents 