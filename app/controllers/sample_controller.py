import uuid

from app.core.exceptions import AppException
from app.repositories import SampleRepository
from app.utils import JwtAuthentication


class SampleController:
    def __init__(
        self, sample_repository: SampleRepository, jwt_authentication: JwtAuthentication
    ):
        self.sample_repository = sample_repository
        self.jwt_authentication = jwt_authentication

    def index(self):
        result = self.sample_repository.index()
        return result

    def save(self, obj_data):
        data = self.sample_repository.create(obj_data)
        return data

    def find(self, obj_id):
        try:
            data = self.sample_repository.get_by_id(obj_id)
        except AppException.NotFoundException:
            raise AppException.BadRequest(error_message="bad operation")
        return data

    def token(self):
        token: dict = self.jwt_authentication.generate_token(user_id=str(uuid.uuid4()))

        return token
