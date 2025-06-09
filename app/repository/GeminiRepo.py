from datetime import datetime
from typing import List, Dict, Tuple
from sqlalchemy import extract, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import MarkdownTextSplitter
from fastapi import HTTPException
import logging
from functools import lru_cache

from app.repository.IGeminiRepo import IGeminiRepo

logger = logging.getLogger(__name__)

class GeminiRepo(IGeminiRepo):
    CHUNK_SIZE = 256
    CHUNK_OVERLAP = 10
    TOP_K_RESULTS = 5
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add(self, text: str) -> bool:
        try:
            return True
        except Exception as e:
            logger.error(f"Error adding text: {str(e)}")
            return False

    @staticmethod
    @lru_cache(maxsize=100)
    def get_embedding_model() -> SentenceTransformer:
        return SentenceTransformer(GeminiRepo.EMBEDDING_MODEL)

    def create_embeddings(self, text: str) -> Tuple[faiss.Index, Dict[int, str]]:
        try:
            model = self.get_embedding_model()
            markdown_splitter = MarkdownTextSplitter(
                chunk_size=self.CHUNK_SIZE,
                chunk_overlap=self.CHUNK_OVERLAP
            )
            docs = markdown_splitter.create_documents([text])
            texts = [doc.page_content for doc in docs]
            
            embeddings = model.encode(texts).astype("float32")

            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            return index, {i: text for i, text in enumerate(texts)}
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