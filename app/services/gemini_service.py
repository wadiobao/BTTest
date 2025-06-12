from fastapi import HTTPException, UploadFile
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from langchain.text_splitter import MarkdownTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import tempfile
import logging
from typing import List, Dict, Any
import asyncio
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.models.chat_request import ChatRequest
from app.utils.data_cleaning import preprocess_text
from app.utils.extract_text import extract_text_from_file
from app.repository.i_gemini_repo import IGeminiRepo

class GeminiService:

    system_instruction_knowledge = """
    Bạn là một trợ lý hỏi đáp tri thức.
Bạn sẽ nhận được hai phần thông tin:
1.  **Câu hỏi của người dùng:** Đây là câu hỏi mà người dùng muốn bạn trả lời.
2.  **Dữ liệu từ cơ sở dữ liệu:** Đây là ngữ cảnh hoặc thông tin mà bạn phải sử dụng để trả lời câu hỏi.

Nhiệm vụ của bạn là trả lời câu hỏi của người dùng CHỈ dựa trên dữ liệu được cung cấp từ cơ sở dữ liệu.

**Các quy tắc:**
-   Nếu thông tin cần thiết để trả lời câu hỏi không có trong dữ liệu, hãy trả lời "Không tìm thấy thông tin liên quan trong dữ liệu."
-   Trả lời ngắn gọn và trực tiếp.
-   Đảm bảo câu trả lời của bạn hoàn toàn dựa vào ngữ cảnh đã cho, không sử dụng kiến thức bên ngoài.
-   Câu trả lời không được có các thông tin bí mật như id
-   Câu trả lời không được chứa tên các biến
-   Câu trả lời không được xuất xứ dữ liệu
    """
    OMNI_PROMPT_TEMPLATE = """
Bạn là một trợ lý AI phân tích và tóm tắt văn bản cực kỳ thông minh. Nhiệm vụ của bạn là dựa vào yêu cầu của người dùng và bối cảnh được cung cấp để đưa ra câu trả lời phù hợp nhất.

Hãy tuân thủ các quy tắc sau:
1.  Phân tích **YÊU CẦU GỐC CỦA NGƯỜI DÙNG**.
2.  Nếu yêu cầu có vẻ là **"có trọng tâm"** (hỏi về một chủ đề, nhân vật, khái niệm cụ thể), hãy sử dụng **BỐI CẢNH** được cung cấp để trả lời chi tiết và chính xác cho câu hỏi đó.
3.  Nếu yêu cầu có vẻ là **"tóm tắt chung"** (ví dụ: "tóm tắt văn bản", "nội dung chính là gì?"), hãy giả định rằng **BỐI CẢNH** là những phần quan trọng và đại diện nhất của toàn bộ tài liệu. Hãy tổng hợp các thông tin trong **BỐI CẢNH** để tạo ra một bản tóm tắt tổng thể.
4.  Luôn trả lời dựa trên thông tin được cung cấp.

---
**BỐI CẢNH (Trích xuất từ tài liệu):**
{context}
---

**YÊU CẦU GỐC CỦA NGƯỜI DÙNG:**
"{user_query}"
---

**CÂU TRẢ LỜI CỦA BẠN:**
"""

    api_key = "AIzaSyDFsMDHe3sYGTV8xLNO14smb2NPrlBLLK8"

    # Configuration
    SUPPORTED_EXTENSIONS = [".md", ".pdf"]
    CHUNK_SIZE = 256
    CHUNK_OVERLAP = 10
    TOP_K_RESULTS = 5
    MODEL_NAME = "gemini-2.0-flash"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    def __init__(self, repo: IGeminiRepo):
        self.repo = repo

    @staticmethod
    @lru_cache(maxsize=100)
    def get_embedding_model():
        return SentenceTransformer(GeminiService.EMBEDDING_MODEL)

    async def process_file(self, file: UploadFile) -> str:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Chỉ hỗ trợ file {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                contents = await file.read()
                temp_file.write(contents)
                temp_file_path = temp_file.name

                unclean_text = extract_text_from_file(temp_file_path)
                
            return preprocess_text(unclean_text), file.filename

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise HTTPException(status_code=500, detail="Lỗi xử lý file")
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)


    async def rag_demo(self, prompt: str) -> str:
        try:
            test_rag = []
            test_rag = await self.repo.query_data(prompt)
            
            context_for_llm = "\n\n---\n\n".join(test_rag)

            print(context_for_llm)
            
            genai.configure(api_key=GeminiService.api_key)
            model = genai.GenerativeModel(model_name="gemini-2.0-flash",system_instruction=context_for_llm)
            response = model.generate_content(prompt)

            return response.text

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in rag_demo: {str(e)}")
            raise HTTPException(status_code=500, detail="Lỗi không xác định")
        
    async def rag_tom_tat(self, prompt: str) -> str:
        try:
            test_rag = []
            test_rag = await self.repo.query_data(prompt)
            
            context_for_llm = "\n\n---\n\n".join(test_rag)
            final_prompt = self.OMNI_PROMPT_TEMPLATE.format(
                context=context_for_llm,
                user_query=prompt
            )
            genai.configure(api_key=GeminiService.api_key)            
            model = genai.GenerativeModel(model_name="gemini-2.0-flash")
            response = model.generate_content(final_prompt)

            return response.text

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in rag_demo: {str(e)}")
            raise HTTPException(status_code=500, detail="Lỗi không xác định")
        
    async def add_file(self, file:UploadFile) -> str:
        try:
        
            clean_text,source = await self.process_file(file)
            
            is_add = await self.repo.add(clean_text,source)
            return is_add

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in rag_demo: {str(e)}")
            raise HTTPException(status_code=500, detail="Lỗi không xác định")

    @staticmethod
    def get_response_with_context_from_database(request: ChatRequest, khoa :str):
        prompt = f"{request.prompt} + {khoa}"
        genai.configure(api_key=GeminiService.api_key)
        config = GenerationConfig(presence_penalty=0.1,frequency_penalty=0.1)
        model1 = genai.GenerativeModel(model_name="gemini-2.0-flash",generation_config=config,system_instruction=GeminiService.system_instruction_knowledge)
        result = model1.generate_content("Tạo 10 câu trả lời và Chọn ra 1 format trả lời xuất hiện nhiều nhất và trả về 1 câu trả lời thuộc format đó" + prompt)

        return result.text

    @staticmethod
    def get_response(request: ChatRequest):
        genai.configure(api_key=GeminiService.api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(request.prompt)
        return response.text
        