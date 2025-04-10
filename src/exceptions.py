from typing import Any, Dict, List

from typing import Optional, Union
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse


class ApiHTTPException(HTTPException):
    """Обработка ошибок API."""

    status_code: int
    code: str
    detail: str

    def __init__(
            self, status_code: Optional[int] = None, detail: Any = None
    ) -> None:
        status_code = status_code or self.status_code
        detail = detail or self.detail
        super().__init__(status_code=status_code, detail=detail)


class ValidationErrorException(ApiHTTPException):
    """Ошибки валидации."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "validation_error"
    detail = "Ошибка валидации."


class ObjectNotFoundException(ApiHTTPException):
    """Объект не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    detail = "Объект не найден."


class ConflictException(ApiHTTPException):
    """Конфликт (например, при бронировании)."""

    status_code = status.HTTP_409_CONFLICT
    code = "conflict"
    detail = "Конфликт с существующими данными."


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Назначение обработчиков исключений.

    :param app:
    :return:
    """

    @app.exception_handler(RequestValidationError)
    async def validation_error(
            request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """
        Обработка ошибок валидации.

        :param request:
        :param exc:
        :return:
        """

        return api_http_exception(ValidationErrorException(detail=exc.errors()))

    @app.exception_handler(ApiHTTPException)
    async def handle_api_exceptions(
            request: Request, exc: ApiHTTPException
    ) -> JSONResponse:
        """
        Обработка ошибок API.

        :param request:
        :param exc:
        :return:
        """

        return api_http_exception(exc)

    @app.exception_handler(Exception)
    async def handle_exceptions(request: Request, exc: Exception) -> JSONResponse:
        """
        Обработка ошибок API.

        :param request:
        :param exc:
        :return:
        """

        return api_exception(exc)


def api_http_exception(exc: ApiHTTPException) -> JSONResponse:
    """
    Форматирование исключения для ответа в API.

    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=format_exception(exc.code, exc.detail),
    )


def api_exception(exc: Exception) -> JSONResponse:
    """
    Форматирование общих исключений для ответа в API.

    :param exc:
    :return:
    """


    code = "server_error"
    description = "Внутренняя ошибка сервера."

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_exception(code, description),
    )


def format_exception(code: str, description: Union[str, Dict]) -> Dict:
    """
    Форматирование исключения.

    :param code:
    :param description:
    :return:
    """
    return {
        "error": {
            "code": code,
            "description": description,
        }
    }


class ValidationErrorDetail(BaseModel):
    key: str
    errors: List[str]
