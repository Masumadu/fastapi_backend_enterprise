import pytest
import fakeredis
from app.core.database import Base, engine, db
from fastapi.testclient import TestClient
from app.models import SampleModel
from app.controllers import SampleController
from app.repositories import SampleRepository
from app.utils import JwtAuthentication
from tests.data import SampleTestData
from datetime import datetime, timedelta
import uuid
import os
from app import constants


@pytest.mark.usefixtures("app")
class BaseTestCase:
    db_instance = db

    @pytest.fixture
    def setup(self, app, mocker):
        config_env = os.getenv("FASTAPI_CONFIG")
        assert config_env == constants.TESTING_ENVIRONMENT, constants.ENV_ERROR.format(config_env)
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # noqa: E501
        self.refresh_token = self.access_token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        Base.metadata.drop_all(bind=engine)
        test_client = TestClient(app)
        self.setup_test_data()
        self.setup_patches(mocker)
        self.instantiate_classes()
        yield test_client

    def setup_test_data(self):
        Base.metadata.create_all(bind=engine)
        self.sample_test_data = SampleTestData()
        self.sample_model = SampleModel(**self.sample_test_data.exiting_sample)
        self.db_instance.add(self.sample_model)
        self.db_instance.commit()

    def instantiate_classes(self):
        self.jwt_authentication = JwtAuthentication()
        self.sample_repository = SampleRepository(redis_service=self.redis)
        self.sample_controller = SampleController(
            sample_repository=self.sample_repository,
            jwt_authentication=self.jwt_authentication
        )

    def setup_patches(self, mocker):
        self.redis = mocker.patch(
            "app.services.redis_service.redis_conn", fakeredis.FakeStrictRedis()
        )
        self.jwt_decode = mocker.patch(
            "app.utils.auth.jwt.decode",
            return_value={
            "id": str(uuid.uuid4()),
            "expires": str(datetime.utcnow() + timedelta(minutes=30))
            }
        )
