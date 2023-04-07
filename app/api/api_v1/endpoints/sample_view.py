from typing import List, Union

import pinject
from fastapi import APIRouter, Depends, status

from app.controllers import SampleController
from app.repositories import SampleRepository
from app.schema import (
    RefreshTokenSchema,
    SampleOutSchema,
    SampleSchema,
    TokenSchema,
    UpdateSampleSchema,
)
from app.services import RedisService
from app.utils import JwtAuthentication

sample_router = APIRouter()

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[SampleController, SampleRepository, RedisService, JwtAuthentication],
)
sample_controller: SampleController = obj_graph.provide(SampleController)


@sample_router.get("/", response_model=Union[List[SampleOutSchema], SampleOutSchema])
def get_resource(resource_id: str = None):
    query_params = {"resource_id": resource_id}
    result = sample_controller.get_resource(query_params)
    return result


@sample_router.post(
    "/", response_model=SampleOutSchema, status_code=status.HTTP_201_CREATED
)
def create_resource(obj_data: SampleSchema):
    result = sample_controller.create_resource(obj_data.dict())
    return result


@sample_router.patch("/{resource_id}", response_model=SampleOutSchema)
def update_resource(
    resource_id: str,
    obj_data: UpdateSampleSchema,
    current_user=Depends(JwtAuthentication()),  # noqa
):
    result = sample_controller.update_resource(resource_id, obj_data.dict())
    return result


@sample_router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: str, current_user=Depends(JwtAuthentication())):  # noqa
    result = sample_controller.delete(resource_id)
    return result


@sample_router.get("/get-token/", response_model=TokenSchema)
def get_token():
    result = sample_controller.get_token()
    return result


@sample_router.post("/refresh-token/", response_model=TokenSchema)
def refresh_token(obj_data: RefreshTokenSchema):
    result = sample_controller.refresh_token(obj_data.dict())
    return result
