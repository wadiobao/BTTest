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

from app.models.request_models.chat_request import ChatRequest
from app.utils.data_cleaning import preprocess_text
from app.utils.extract_text import extract_text_from_file
from app.repository.gemini_repo.i_gemini_repo import IGeminiRepo

class GeminiService:

    system_instruction_knowledge = """
    You are a knowledge Q&A assistant.
You will receive two pieces of information:
1.  **User's question:** This is the question the user wants you to answer.
2.  **Data from the database:** This is the context or information you must use to answer the question.

Your task is to answer the user's question ONLY based on the data provided from the database.

**Rules:**
-   If the information needed to answer the question is not in the data, reply "No relevant information found in the data."
-   Answer concisely and directly.
-   Ensure your answer is entirely based on the given context, do not use outside knowledge.
-   The answer must not contain confidential information such as IDs.
-   The answer must not contain variable names.
-   The answer must not mention data sources.
    """
    OMNI_PROMPT_TEMPLATE = """
You are an extremely intelligent AI assistant for analyzing and summarizing text. Your task is to use the user's request and the provided context to give the most appropriate answer.

Please follow these rules:
1.  Analyze the **USER'S ORIGINAL REQUEST**.
2.  If the request seems **"focused"** (asking about a specific topic, person, or concept), use the **CONTEXT** provided to answer that question in detail and accurately.
3.  If the request seems like a **"general summary"** (e.g., "general summary", "what is it about", "main details", "what is the main content?", "summarize", "overview", "summarize", "write about", "topic", "purpose", "mention", "what's in this file", "key point", "main idea", "argument", "conclusion", "overview"), assume that the **CONTEXT** is the most important and representative part of the entire document. Synthesize the information in the **CONTEXT** to create an overall summary.
4.  Always answer based on the information provided.

---
**CONTEXT (Extracted from the document):**
{context}
---

**USER'S ORIGINAL REQUEST:**
"{user_query}"
---

**YOUR ANSWER:**
"""

    api_key = "AIzaSyDFsMDHe3sYGTV8xLNO14smb2NPrlBLLK8"

    # Configuration
    SUPPORTED_EXTENSIONS = [".md", ".pdf",".txt"]
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
                detail=f"Only support files: {', '.join(self.SUPPORTED_EXTENSIONS)}"
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
            raise HTTPException(status_code=500, detail="File processing error")
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
            model = genai.GenerativeModel(model_name=self.MODEL_NAME,system_instruction=context_for_llm)
            response = model.generate_content(prompt)

            return response.text

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in rag_demo: {str(e)}")
            raise HTTPException(status_code=500, detail="Unknown error")
        
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
            raise HTTPException(status_code=500, detail="Unknown error")
        
    async def add_file(self, file:UploadFile) -> str:
        try:
        
            clean_text,source = await self.process_file(file)
            
            is_add = await self.repo.add(clean_text,source)
            return is_add

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in rag_demo: {str(e)}")
            raise HTTPException(status_code=500, detail="Unknown error")

    @staticmethod
    def get_response_with_context_from_database(request: ChatRequest, khoa :str):
        prompt = f"{request.prompt} + {khoa}"
        genai.configure(api_key=GeminiService.api_key)
        config = GenerationConfig(presence_penalty=0.1,frequency_penalty=0.1)
        model1 = genai.GenerativeModel(model_name="gemini-2.0-flash",generation_config=config,system_instruction=GeminiService.system_instruction_knowledge)
        result = model1.generate_content("Generate 10 answers, select the most common answer format, and return one answer in that format." + prompt)

        return result.text

    @staticmethod
    def get_response(request: ChatRequest):
        genai.configure(api_key=GeminiService.api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(request.prompt)
        return response.text
