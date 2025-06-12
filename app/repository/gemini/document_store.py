import logging
from typing import List, Tuple
from langchain.storage import LocalFileStore
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)

class DocumentStore:
    def __init__(self, db_path: str):
        self.store = LocalFileStore(db_path)
    
    async def store_parent_chunks(
        self, 
        parent_chunks: List[Document], 
        parent_ids: List[str]
    ) -> None:
        """
        Lưu các parent chunks vào document store.
        """
        docs_to_store: List[Tuple[str, bytes]] = []
        for i, chunk in enumerate(parent_chunks):
            encoded_content = chunk.page_content.encode('utf-8')
            docs_to_store.append((parent_ids[i], encoded_content))
        
        await self.store.amset(docs_to_store)
        logger.info(f"Đã lưu {len(parent_chunks)} parent chunks vào LocalFileStore")
    
    async def get_parent_chunks(self, parent_ids: List[str]) -> List[str]:
        """
        Lấy nội dung của các parent chunks từ document store.
        """
        parent_docs_bytes = await self.store.amget(parent_ids)
        return [
            doc_bytes.decode('utf-8') 
            for doc_bytes in parent_docs_bytes if doc_bytes is not None
        ] 