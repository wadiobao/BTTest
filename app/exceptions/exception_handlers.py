import os
import re
from typing import Any, List, Optional, Set
from fastapi import Body, Depends, FastAPI, HTTPException, Header, Path, Request, status, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.response_models import ApiResponse, ResponseException

def setup_exception_handlers(app: FastAPI):
    """Setup custom exception handlers for the FastAPI application"""

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        """
        Custom exception handler để định dạng lại lỗi xác thực Pydantic.
        Cố gắng lấy thông báo lỗi cụ thể từ lỗi đầu tiên.
        """

        # Mặc định là một thông báo chung
        error_message_to_display = "Dữ liệu đầu vào không hợp lệ. Vui lòng kiểm tra các trường đã gửi."

        # Cố gắng lấy thông báo lỗi cụ thể từ lỗi đầu tiên nếu có
        if exc.errors():
            first_error = exc.errors()[0]
            # Lấy msg từ lỗi đầu tiên.
            # Hoặc có thể lấy thông báo lỗi từ ctx['error'] nếu đó là ValueError từ custom validator
            if 'msg' in first_error:
                # Pydantic v2 thường có 'msg' chứa thông báo lỗi tổng quát (e.g., "Value error, Giới tính phải là 'Nam' hoặc 'Nữ'")
                # và 'ctx' chứa đối tượng lỗi gốc.
                # Bạn có thể chọn cái nào phù hợp hơn.
                # Ở đây, tôi sẽ ưu tiên thông báo từ ctx['error'] nếu nó là ValueError gốc.
                if 'ctx' in first_error and 'error' in first_error['ctx'] and isinstance(first_error['ctx']['error'], ValueError):
                    error_message_to_display = str(first_error['ctx']['error'])
                else:
                    error_message_to_display = first_error['msg']
            elif 'type' in first_error:
                error_message_to_display = f"Lỗi xác thực kiểu dữ liệu: {first_error['type']}"

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": error_message_to_display, # Sử dụng thông báo lỗi cụ thể
                # "timestamp": datetime.now().isoformat() # Tùy chọn
            },
        )
        
    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        custom_error_response = ApiResponse(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            status="error",
            result=str(exc)
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=custom_error_response.model_dump()
        )
        
    @app.exception_handler(TypeError)
    async def handle_type_error(request: Request, exc: TypeError):
        custom_error_response = ApiResponse(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            status="error",
            result=str(exc)
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=custom_error_response.model_dump()
        )

    @app.exception_handler(AttributeError)
    async def handle_attribute_error(request: Request, exc: AttributeError):
        custom_error_response = ApiResponse(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            status="error",
            result=str(exc)
        )
        
        return JSONResponse(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            content=custom_error_response.model_dump()
        )

    @app.exception_handler(ResponseException)
    async def handle_response_exception(request: Request, exc: ResponseException):
        custom_error_response = ApiResponse(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            status="error",
            result=exc.message
        )
        
        return JSONResponse(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            content=custom_error_response.model_dump()
        ) 
