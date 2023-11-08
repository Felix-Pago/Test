"""
    This a simple endpoint definition example. You can delete this file (make sure to also delete the
    related configurations on app/bootstrap/bootstrapper.py also).
"""
from typing import Dict

from fastapi import APIRouter

from app.services.example_service import ExampleService

router: APIRouter = APIRouter()


@router.get('/')
async def example() -> Dict[str, str]:
    return ExampleService.flow_execution_example()
