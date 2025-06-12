import uuid
import logging
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)

class TextSplitter:
    def __init__(
        self,
        chunk_size_parent: int = 5000,
        chunk_overlap_parent: int = 1500,
        chunk_size_child: int = 1000,
        chunk_overlap_child: int = 300
    ):
        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size_parent,
            chunk_overlap=chunk_overlap_parent
        )
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size_child,
            chunk_overlap=chunk_overlap_child
        )
    
    def split_parent(self, text: str, source: str) -> Tuple[List[Document], List[str]]:
        """
        Chia văn bản thành các parent chunks.
        """
        parent_chunks = self.parent_splitter.create_documents(
            [text], 
            metadatas=[{"source": source}]
        )
        parent_ids = [str(uuid.uuid4()) for _ in parent_chunks]
        
        logger.info(f"Đã chia thành {len(parent_chunks)} parent chunks từ nguồn '{source}'")
        return parent_chunks, parent_ids
    
    def split_children(
        self, 
        parent_chunks: List[Document], 
        parent_ids: List[str],
        source: str
    ) -> List[Document]:
        """
        Chia các parent chunks thành child chunks.
        """
        all_child_chunks = []
        for i, parent_chunk in enumerate(parent_chunks):
            parent_id = parent_ids[i]
            sub_chunks = self.child_splitter.split_documents([parent_chunk])
            for child_chunk in sub_chunks:
                child_chunk.metadata["parent_id"] = parent_id
                child_chunk.metadata["source"] = source
            all_child_chunks.extend(sub_chunks)
        
        logger.info(f"Đã chia thành {len(all_child_chunks)} child chunks từ nguồn '{source}'")
        return all_child_chunks 