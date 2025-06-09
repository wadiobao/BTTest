import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
import os

from app.models.ChatRequest import ChatRequest
from app.models.MainModels import Khoa, SinhVien, LopHoc
from app.services.KhoaService import KhoaService
from app.utils.mapper import map_khoa_to_response, map_sinhvien_to_response

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
    system_instruction_consistency = """
    Bạn là một nhà phân tích nội dung
    Nhiệm vụ của bạn là phân tích nội dung của câu trả lời và đảm bảo nó
    -   Không có thông tin bí mật
    -   Không có tên các biến
    -   Không có thông tin xuất xứ dữ liệu
    -   Có thể trả lời câu hỏi của người dùng

    Bạn sẽ nhận được 1 danh sách câu trả lời

    Bạn sẽ phải phân tích và đánh giá các câu trả lời và chọn 1 format câu trả lời mà có số câu trả lời có nhiều nhất

    Output: [nội dung chính câu trả lời theo format đã chọn]

    """

    api_key = "AIzaSyDFsMDHe3sYGTV8xLNO14smb2NPrlBLLK8"

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