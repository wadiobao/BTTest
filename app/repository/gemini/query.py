import logging
from typing import Any, List, Optional
from langchain.docstore.document import Document
from sentence_transformers.cross_encoder import CrossEncoder
from rank_bm25 import BM25Okapi
import numpy as np

from app.repository.gemini.vector_store import VectorStore
from app.repository.gemini.document_store import DocumentStore

logger = logging.getLogger(__name__)

class QueryHandler:
    def __init__(
        self,
        vector_store: VectorStore,
        document_store: DocumentStore,
        top_k_results: int = 100,
        rerank_top_k: int = 20
    ):
        self.vector_store = vector_store
        self.document_store = document_store
        self.top_k_results = top_k_results
        self.rerank_top_k = rerank_top_k
        self.reranker = CrossEncoder('cross-encoder/ms-marco-minilm-l-6-v2')
    
    async def query(
        self, 
        query: str, 
        source_document: Optional[str] = None
    ) -> List[str]:
        """
        Process query and return results.
        """
        try:
            # 1. Kiểm tra sources trong database
            all_sources = self.vector_store.get_all_sources()
            logger.info(f"Các sources có trong database: {all_sources}")
            
            # 2. Kiểm tra xem query có chứa tên file không
            matching_sources = []
            for source in all_sources:
                source_name = source.lower().replace('.pdf', '')
                if source_name in query.lower():
                    matching_sources.append(source)
            
            logger.info(f"Các sources khớp với query: {matching_sources}")
            
            # 3. Xác định source để tìm kiếm
            search_source = None
            if source_document:
                search_source = source_document
                logger.info(f"Tìm kiếm trong source được chỉ định: {search_source}")
            elif matching_sources:
                search_source = matching_sources[0]
                logger.info(f"Tìm kiếm trong source khớp với query: {search_source}")
            
            # 4. Tìm kiếm trong vector store
            child_docs = await self.vector_store.search(
                query=query,
                k=self.top_k_results,
                source_document=search_source
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

            # 5. Lấy parent documents
            parent_ids = [doc.metadata["parent_id"] for doc in child_docs if "parent_id" in doc.metadata]
            unique_parent_ids = list(dict.fromkeys(parent_ids))
            logger.info(f"Số lượng parent_ids unique: {len(unique_parent_ids)}")
            logger.info(f"Danh sách parent_ids: {unique_parent_ids}")

            # 6. Lấy nội dung parent documents
            parent_contents = await self.document_store.get_parent_chunks(unique_parent_ids)
            logger.info(f"Số lượng parent documents lấy được: {len(parent_contents)}")
            
            return parent_contents

        except Exception as e:
            logger.error(f"Error in hybrid query: {e}", exc_info=True)
            return [] 
        
    async def hybrid_query(
        self,
        query: str,
        source_document: Optional[str] = None,
        dense_weight: float = 0.7,
        sparse_weight: float = 0.3
    ) -> List[str]:
        """
        Thực hiện hybrid search kết hợp dense và sparse retrieval.
        
        Args:
            query: Câu query cần tìm kiếm
            source_document: Tài liệu nguồn cụ thể (nếu có)
            dense_weight: Trọng số cho dense retrieval (0-1)
            sparse_weight: Trọng số cho sparse retrieval (0-1)
            
        Returns:
            List[str]: Danh sách các kết quả tìm được
        """
        try:
            # 1. Lấy tất cả documents từ vector store
            all_docs = await self.vector_store.get_all_documents(source_document)
            if not all_docs:
                return []
                
            # 2. Thực hiện dense retrieval (vector search)
            dense_docs = await self.vector_store.search(
                query=query,
                k=self.top_k_results,
                source_document=source_document
            )
            
            # 3. Thực hiện sparse retrieval (BM25)
            # Chuẩn bị corpus cho BM25
            corpus = [doc.page_content for doc in all_docs]
            tokenized_corpus = [doc.split() for doc in corpus]
            bm25 = BM25Okapi(tokenized_corpus)
            
            # Tính điểm BM25
            tokenized_query = query.split()
            bm25_scores = bm25.get_scores(tokenized_query)
            
            # Chuẩn hóa điểm BM25 về thang 0-1
            bm25_scores = (bm25_scores - np.min(bm25_scores)) / (np.max(bm25_scores) - np.min(bm25_scores))
            
            # 4. Kết hợp kết quả
            combined_scores = {}
            
            # Thêm điểm dense retrieval
            for doc in dense_docs:
                doc_id = doc.metadata.get("parent_id")
                if doc_id:
                    combined_scores[doc_id] = dense_weight
                    
            # Thêm điểm sparse retrieval
            for idx, score in enumerate(bm25_scores):
                doc = all_docs[idx]
                doc_id = doc.metadata.get("parent_id")
                if doc_id:
                    if doc_id in combined_scores:
                        combined_scores[doc_id] += sparse_weight * score
                    else:
                        combined_scores[doc_id] = sparse_weight * score
                        
            # 5. Sort results by score
            sorted_doc_ids = sorted(
                combined_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:self.rerank_top_k]
            
            # 6. Lấy nội dung parent documents
            parent_ids = [doc_id for doc_id, _ in sorted_doc_ids]
            parent_contents = await self.document_store.get_parent_chunks(parent_ids)
            
            logger.info(f"Hybrid search completed. Found {len(parent_contents)} results")
            return parent_contents
            
        except Exception as e:
            logger.error(f"Error in hybrid query: {e}", exc_info=True)
            return []
            
