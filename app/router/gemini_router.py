from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlmodel.ext.asyncio.session import AsyncSession
from app.exceptions import ApiResponse
from app.services.gemini_service import GeminiService
from app.database import get_session
from app.repository.gemini import GeminiRepo
from app.repository.gemini.document_store import DocumentStore

async def get_gemini_service(session: AsyncSession = Depends(get_session)) -> GeminiService:
    repo = GeminiRepo(session)
    return GeminiService(repo)

router = APIRouter(prefix="/chat")

@router.post("/demo-rag/")
async def demo_rag(prompt: str = Form(...), gemini_service: GeminiService = Depends(get_gemini_service)):
    response = await gemini_service.rag_demo(prompt=prompt)
    return ApiResponse(code=status.HTTP_200_OK, result=response)

@router.post("/add/")
async def add_file(file: UploadFile = File(...), gemini_service: GeminiService = Depends(get_gemini_service)):
    response = await gemini_service.add_file(file=file)
    return ApiResponse(code=status.HTTP_200_OK, result=response)

@router.post("/summary/")
async def rag_summary(prompt: str = Form(...), gemini_service: GeminiService = Depends(get_gemini_service)):
    response = await gemini_service.rag_tom_tat(prompt=prompt)
    return ApiResponse(code=status.HTTP_200_OK, result=response) 