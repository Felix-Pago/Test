from typing import Any, Dict, Union

from pydantic import BaseModel


class ApplicationError(BaseModel):
    message: str


def get_error_responses_schema() -> Dict[Union[int, str], Dict[str, Any]]:
    return {400: {"model": ApplicationError},
            401: {"model": ApplicationError},
            403: {"model": ApplicationError},
            404: {"model": ApplicationError},
            422: {"model": ApplicationError},
            500: {"model": ApplicationError}}
