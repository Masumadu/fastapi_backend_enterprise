from typing import List

import pinject
from fastapi import APIRouter, Depends, status

from app.controllers import SampleController
from app.repositories import SampleRepository
from app.schema import AuthSchema, SampleOutSchema, SampleSchema, TokenSchema
from app.services import RedisService
from app.utils import JwtAuthentication

sample_router = APIRouter()

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[SampleController, SampleRepository, RedisService, JwtAuthentication],
)
sample_controller: SampleController = obj_graph.provide(SampleController)


@sample_router.get("/get-all/", response_model=List[SampleOutSchema])
def index():
    result = sample_controller.index()
    return result


@sample_router.get("/get/{id}", response_model=SampleOutSchema)
def find(id: str):
    result = sample_controller.find(id)
    return result


@sample_router.post(
    "/create/", response_model=SampleOutSchema, status_code=status.HTTP_201_CREATED
)
def create(data: SampleSchema):
    result = sample_controller.save(data.dict())
    return result


@sample_router.post("/token/", response_model=TokenSchema)
def token():
    result = sample_controller.token()
    return result


@sample_router.post("/auth/", response_model=AuthSchema)
def protected(current_user=Depends(JwtAuthentication())):  # noqa
    return {"user_id": current_user}
