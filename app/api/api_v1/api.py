from fastapi import FastAPI

from .endpoints import sample_router


def init_api_v1(app: FastAPI):
    app.include_router(
        router=sample_router, tags=["SampleRoute"], prefix="/api/v1/sample-resource"
    )
