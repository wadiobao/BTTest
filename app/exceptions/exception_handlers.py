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
        Custom exception handler to format Pydantic validation errors.
        Attempts to get a specific error message from the first error.
        """

        # Mặc định là một thông báo chung
        error_message_to_display = "Invalid input data. Please check your submitted fields."

        # Cố gắng lấy thông báo lỗi cụ thể từ lỗi đầu tiên nếu có
        if exc.errors():
            first_error = exc.errors()[0]
            # Get msg from the first error.
            # Or you can get the error message from ctx['error'] if it's a ValueError from a custom validator
            if 'msg' in first_error:
                # Pydantic v2 usually has 'msg' containing a general error message (e.g., "Value error, Gender must be 'Nam' or 'Nữ'")
                # and 'ctx' containing the original error object.
                # You can choose which one is more appropriate.
                # Here, I will prioritize the message from ctx['error'] if it is the original ValueError.
                if 'ctx' in first_error and 'error' in first_error['ctx'] and isinstance(first_error['ctx']['error'], ValueError):
                    error_message_to_display = str(first_error['ctx']['error'])
                else:
                    error_message_to_display = first_error['msg']
            elif 'type' in first_error:
                error_message_to_display = f"Data type validation error: {first_error['type']}"

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": error_message_to_display,
            },
        )
        
    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": str(exc),
            },
        )
        
    @app.exception_handler(TypeError)
    async def handle_type_error(request: Request, exc: TypeError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": str(exc),
            },
        )

    @app.exception_handler(AttributeError)
    async def handle_attribute_error(request: Request, exc: AttributeError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": str(exc),
            },
        )

    @app.exception_handler(ResponseException)
    async def handle_response_exception(request: Request, exc: ResponseException):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": exc.message,
            },
        ) 
