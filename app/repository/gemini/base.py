import os
import logging
from typing import List, Dict, Optional, Tuple, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.storage import LocalFileStore
import chromadb
import faiss
from functools import lru_cache
from sentence_transformers import SentenceTransformer

from app.repository.i_gemini_repo import IGeminiRepo
from app.repository.gemini.text_splitter import TextSplitter
from app.repository.gemini.vector_store import VectorStore
from app.repository.gemini.document_store import DocumentStore
from app.repository.gemini.query import QueryHandler

logger = logging.getLogger(__name__)

class GeminiRepo(IGeminiRepo):
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    def __init__(
        self,
        session: AsyncSession,
        db_path: str = "parent_child_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size_parent: int = 1024,
        chunk_overlap_parent: int = 100,
        chunk_size_child: int = 128,
        chunk_overlap_child: int = 12,
        top_k_results: int = 100
    ):
        """
        Khởi tạo tất cả các thành phần cần thiết một lần duy nhất.
        """
        self.top_k_results = top_k_results
        self.session = session
        
        # Đảm bảo db_path là string
        if not isinstance(db_path, str):
            raise ValueError("db_path phải là một chuỗi đường dẫn")
            
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(db_path, exist_ok=True)
        
        # Khởi tạo các thành phần
        self.text_splitter = TextSplitter(
            chunk_size_parent=chunk_size_parent,
            chunk_overlap_parent=chunk_overlap_parent,
            chunk_size_child=chunk_size_child,
            chunk_overlap_child=chunk_overlap_child
        )
        
        self.vector_store = VectorStore(
            db_path=db_path,
            embedding_model=embedding_model
        )
        
        self.document_store = DocumentStore(db_path=db_path)
        self.query_handler = QueryHandler(
            vector_store=self.vector_store,
            document_store=self.document_store,
            top_k_results=self.top_k_results
        )
    
    @staticmethod
    @lru_cache(maxsize=100)
    def get_embedding_model() -> SentenceTransformer:
        """
        Lấy model embedding với cache.
        """
        return SentenceTransformer(GeminiRepo.EMBEDDING_MODEL)
    
    def create_embeddings(self, text: str) -> Tuple[faiss.Index, Dict[int, str]]:
        """
        Tạo embeddings cho văn bản.
        """
        try:
            if not text or not text.strip():
                raise ValueError("Văn bản trống hoặc không hợp lệ")

            model = self.get_embedding_model()
            chunks = self.text_splitter.split_parent(text, "temp")[0]
            
            if not chunks:
                raise ValueError("Không thể tách văn bản thành các đoạn nhỏ")
            
            embeddings = model.encode([chunk.page_content for chunk in chunks]).astype("float32")
            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            return index, {i: chunk.page_content for i, chunk in enumerate(chunks)}
            
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise
        
    def search_similar_texts(
        self,
        query: str,
        index: faiss.Index,
        id_to_text: Dict[int, str]
    ) -> List[str]:
        """
        Tìm kiếm văn bản tương tự.
        """
        try:
            model = self.get_embedding_model()
            query_embedding = model.encode([query]).astype("float32")
            D, I = index.search(query_embedding, self.top_k_results)
            return [id_to_text[idx] for idx in I[0]]
        except Exception as e:
            logger.error(f"Error searching similar texts: {str(e)}")
            raise
        
    async def add(self, text: str, source: str) -> bool:
        """
        Thêm văn bản mới vào hệ thống.
        """
        try:
            # 1. Chia văn bản thành các chunks
            parent_chunks, parent_ids = self.text_splitter.split_parent(text, source)
            
            # 2. Lưu parent chunks
            await self.document_store.store_parent_chunks(parent_chunks, parent_ids)
            
            # 3. Tạo và lưu child chunks
            child_chunks = self.text_splitter.split_children(parent_chunks, parent_ids, source)
            if child_chunks:
                await self.vector_store.store_child_chunks(child_chunks)
            
            return True
            
        except Exception as e:
            logger.error(f"Lỗi khi thêm tài liệu từ '{source}': {e}", exc_info=True)
            return False
            
    async def query_data(self, query: str, source_document: Optional[str] = None) -> List[str]:
        """
        Query data.
        """
        return await self.query_handler.hybrid_query(query, source_document) 
    
    