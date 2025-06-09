from abc import ABC, abstractmethod
from typing import Any, List, Dict, Tuple
import faiss

from annotated_types import T

class IGeminiRepo(ABC):
    
    @abstractmethod
    async def add(self, text: str) -> bool:
        pass

    @abstractmethod
    def create_embeddings(self, text: str) -> Tuple[faiss.Index, Dict[int, str]]:
        pass

    @abstractmethod
    def search_similar_texts(
        self,
        query: str,
        index: faiss.Index,
        id_to_text: Dict[int, str]
    ) -> List[str]:
        pass

    @abstractmethod
    def get_embedding_model(self) -> Any:
        pass