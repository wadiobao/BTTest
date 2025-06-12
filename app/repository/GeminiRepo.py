from datetime import datetime
import os
from typing import List, Dict, Optional, Tuple
from sqlalchemy import extract, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
import chromadb
from chromadb.utils import embedding_functions
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import MarkdownTextSplitter,RecursiveCharacterTextSplitter
from fastapi import HTTPException
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.storage import InMemoryStore,LocalFileStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import logging
import uuid
from functools import lru_cache

from app.repository.IGeminiRepo import IGeminiRepo

logger = logging.getLogger(__name__)

class GeminiRepo(IGeminiRepo):
    CHUNK_SIZE_PARENT = 1500
    CHUNK_OVERLAP_PARENT = 200
    CHUNK_SIZE_CHILD = 500
    CHUNK_OVERLAP_CHILD = 60
    TOP_K_RESULTS = 10
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    def __init__(
        self,
        session: AsyncSession,
        db_path: str = "parent_child_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size_parent: int = 5000,
        chunk_overlap_parent: int = 1500,
        chunk_size_child: int = 1000,
        chunk_overlap_child: int = 300,
        top_k_results: int = 5
    ):
        """
        Khởi tạo tất cả các thành phần cần thiết một lần duy nhất.
        
        Args:
            db_path (str): Đường dẫn đến thư mục lưu trữ database. Mặc định là "parent_child_db"
            embedding_model (str): Tên model embedding để sử dụng
            chunk_size_parent (int): Kích thước chunk cha
            chunk_overlap_parent (int): Độ chồng lấp của chunk cha
            chunk_size_child (int): Kích thước chunk con
            chunk_overlap_child (int): Độ chồng lấp của chunk con
            top_k_results (int): Số lượng kết quả trả về khi tìm kiếm
        """
        self.TOP_K_RESULTS = top_k_results
        self.session = session

        # Đảm bảo db_path là string
        if not isinstance(db_path, str):
            raise ValueError("db_path phải là một chuỗi đường dẫn")
            
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(db_path, exist_ok=True)
        
        # 1. Khởi tạo các splitter
        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size_parent,
            chunk_overlap=chunk_overlap_parent
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size_child,
            chunk_overlap=chunk_overlap_child
        )

        # 2. Khởi tạo embedding function
        self.embedding_function = HuggingFaceEmbeddings(model_name=embedding_model)

        # 3. Khởi tạo Vectorstore (lưu chunk con)
        # Sử dụng Chroma client trực tiếp để quản lý tốt hơn
        db_client = chromadb.PersistentClient(path=db_path)
        self.vectorstore = Chroma(
            client=db_client,
            collection_name="child_chunks_for_search",
            embedding_function=self.embedding_function,
        )

        # 4. Khởi tạo Document Store (lưu chunk cha)
        self.docstore = LocalFileStore(db_path)
        
    async def add(self, text: str, source: str) -> bool:
        try:
            # GIAI ĐOẠN 1: XỬ LÝ CHUNK CHA
            parent_chunks = self.parent_splitter.create_documents([text], metadatas=[{"source": source}])
            parent_ids = [str(uuid.uuid4()) for _ in parent_chunks]
            
            # Log metadata của parent chunks
            for i, chunk in enumerate(parent_chunks):
                logger.info(f"Parent chunk {i+1} metadata: {chunk.metadata}")
                logger.info(f"Parent chunk {i+1} content: {chunk.page_content[:200]}...")
            
            # CHUẨN BỊ DỮ LIỆU ĐỂ LƯU
            docs_to_store: List[Tuple[str, bytes]] = []
            for i, chunk in enumerate(parent_chunks):
                encoded_content = chunk.page_content.encode('utf-8')
                docs_to_store.append((parent_ids[i], encoded_content))
            
            await self.docstore.amset(docs_to_store)
            logger.info(f"Đã lưu {len(parent_chunks)} chunk cha từ '{source}' vào LocalFileStore.")

            # GIAI ĐOẠN 2: XỬ LÝ CHUNK CON
            all_child_chunks = []
            for i, parent_chunk in enumerate(parent_chunks):
                parent_id = parent_ids[i]
                sub_chunks = self.child_splitter.split_documents([parent_chunk])
                for child_chunk in sub_chunks:
                    child_chunk.metadata["parent_id"] = parent_id
                    child_chunk.metadata["source"] = source
                all_child_chunks.extend(sub_chunks)

            if all_child_chunks:
                child_ids = [str(uuid.uuid4()) for _ in all_child_chunks]
                
                # Log metadata của child chunks trước khi lưu
                for i, chunk in enumerate(all_child_chunks):
                    logger.info(f"Child chunk {i+1} metadata: {chunk.metadata}")
                    logger.info(f"Child chunk {i+1} content: {chunk.page_content[:200]}...")
                
                await self.vectorstore.aadd_documents(documents=all_child_chunks, ids=child_ids)
                logger.info(f"Đã thêm {len(all_child_chunks)} chunk con từ '{source}' vào ChromaDB.")
                
                # Thêm logging để kiểm tra số lượng documents trong ChromaDB
                collection = self.vectorstore._collection
                count = collection.count()
                logger.info(f"Tổng số documents trong ChromaDB sau khi thêm: {count}")
                
                # Log tất cả documents trong ChromaDB
                results = collection.get()
                if results and results['metadatas']:
                    logger.info("Metadata của tất cả documents trong ChromaDB:")
                    for i, metadata in enumerate(results['metadatas']):
                        logger.info(f"Document {i+1} metadata: {metadata}")
            
            return True

        except Exception as e:
            logger.error(f"Lỗi khi thêm tài liệu từ '{source}': {e}", exc_info=True)
            return False

    @staticmethod
    @lru_cache(maxsize=100)
    def get_embedding_model() -> SentenceTransformer:
        return SentenceTransformer(GeminiRepo.EMBEDDING_MODEL)

    def create_embeddings(self, text: str) -> Tuple[faiss.Index, Dict[int, str]]:
        try:
            if not text or not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Văn bản trống hoặc không hợp lệ"
                )

            model = self.get_embedding_model()
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.CHUNK_SIZE,
                chunk_overlap=self.CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
            )
            
            chunks = splitter.split_text(text)
            
            if not chunks:
                raise HTTPException(
                    status_code=400,
                    detail="Không thể tách văn bản thành các đoạn nhỏ"
                )
            
            embeddings = model.encode(chunks).astype("float32")

            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            return index, {i: chunk for i, chunk in enumerate(chunks)}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise HTTPException(status_code=500, detail="Lỗi tạo embeddings")

    def search_similar_texts(
        self,
        query: str,
        index: faiss.Index,
        id_to_text: Dict[int, str]
    ) -> List[str]:
        try:
            model = self.get_embedding_model()
            query_embedding = model.encode([query]).astype("float32")
            D, I = index.search(query_embedding, self.TOP_K_RESULTS)
            return [id_to_text[idx] for idx in I[0]]
        except Exception as e:
            logger.error(f"Error searching similar texts: {str(e)}")
            raise HTTPException(status_code=500, detail="Lỗi tìm kiếm văn bản tương tự") 
        
    async def query_data(self, query: str, source_document: Optional[str] = None) -> List[str]:
        """
        Truy vấn dữ liệu, xử lý đúng trường hợp có và không có bộ lọc.
        """
        try:
            # Log số lượng documents hiện có trong ChromaDB
            collection = self.vectorstore._collection
            total_docs = collection.count()
            logger.info(f"Tổng số documents trong ChromaDB trước khi query: {total_docs}")
            
            # Lấy tất cả documents để kiểm tra sources
            all_docs = collection.get()
            if all_docs and all_docs['metadatas']:
                unique_sources = set()
                for metadata in all_docs['metadatas']:
                    if 'source' in metadata:
                        unique_sources.add(metadata['source'])
                logger.info(f"Các sources có trong database: {unique_sources}")
            
            # Kiểm tra xem query có chứa tên file không
            matching_sources = []
            for source in unique_sources:
                # Loại bỏ phần mở rộng .pdf và chuyển về chữ thường để so sánh
                source_name = source.lower().replace('.pdf', '')
                if source_name in query.lower():
                    matching_sources.append(source)
            
            logger.info(f"Các sources khớp với query: {matching_sources}")
            
            # 1. Chuẩn bị các tham số cho việc tìm kiếm
            search_kwargs = {
                'k': self.TOP_K_RESULTS
            }
            
            # 2. Xây dựng và thêm mệnh đề lọc
            if source_document:
                # Nếu có source_document được chỉ định, ưu tiên tìm trong source đó
                filter_clause = {"source": source_document}
                search_kwargs['filter'] = filter_clause
                logger.info(f"Thực hiện query có lọc theo source được chỉ định: '{source_document}'")
            elif matching_sources:
                # Nếu query chứa tên file, ưu tiên tìm trong file đó
                filter_clause = {"source": matching_sources[0]}
                search_kwargs['filter'] = filter_clause
                logger.info(f"Thực hiện query có lọc theo tên file trong query: '{matching_sources[0]}'")
            else:
                logger.info("Thực hiện query trên tất cả các tài liệu (không lọc).")
            
            # 3. Gọi hàm tìm kiếm
            child_docs = await self.vectorstore.asimilarity_search(
                query,
                **search_kwargs
            )
            
            logger.info(f"Số lượng kết quả tìm thấy: {len(child_docs)}")
            
            # Log metadata và nội dung của các documents tìm thấy
            sources_found = set()
            for i, doc in enumerate(child_docs):
                logger.info(f"Document {i+1} metadata: {doc.metadata}")
                logger.info(f"Document {i+1} content: {doc.page_content[:200]}...")
                if 'source' in doc.metadata:
                    sources_found.add(doc.metadata['source'])
            
            logger.info(f"Các sources được tìm thấy trong kết quả: {sources_found}")

            if not child_docs:
                return []

            parent_ids = [doc.metadata["parent_id"] for doc in child_docs if "parent_id" in doc.metadata]
            unique_parent_ids = list(dict.fromkeys(parent_ids))
            logger.info(f"Số lượng parent_ids unique: {len(unique_parent_ids)}")
            logger.info(f"Danh sách parent_ids: {unique_parent_ids}")

            parent_docs_bytes = await self.docstore.amget(unique_parent_ids)
            logger.info(f"Số lượng parent documents lấy được từ docstore: {len([x for x in parent_docs_bytes if x is not None])}")
            
            # Log thông tin về các parent documents
            for i, doc_bytes in enumerate(parent_docs_bytes):
                if doc_bytes is not None:
                    content = doc_bytes.decode('utf-8')
                    logger.info(f"Parent document {i+1} content: {content[:200]}...")
            
            return [
                doc_bytes.decode('utf-8') 
                for doc_bytes in parent_docs_bytes if doc_bytes is not None
            ]

        except Exception as e:
            logger.error(f"Lỗi khi truy vấn: {e}", exc_info=True)
            return []