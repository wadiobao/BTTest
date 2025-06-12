import logging
from typing import List, Optional
from langchain.docstore.document import Document

from app.repository.gemini.vector_store import VectorStore
from app.repository.gemini.document_store import DocumentStore

logger = logging.getLogger(__name__)

class QueryHandler:
    def __init__(
        self,
        vector_store: VectorStore,
        document_store: DocumentStore,
        top_k_results: int = 5
    ):
        self.vector_store = vector_store
        self.document_store = document_store
        self.top_k_results = top_k_results
    
    async def query(
        self, 
        query: str, 
        source_document: Optional[str] = None
    ) -> List[str]:
        """
        Xử lý query và trả về kết quả.
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
            logger.error(f"Lỗi khi truy vấn: {e}", exc_info=True)
            return [] 