import pytest
from tests.base_test_case import BaseTestCase
from app.models import SampleModel
from app.core.exceptions import AppException
import uuid


class TestSampleController(BaseTestCase):
    @pytest.mark.controller
    def test_index(self, setup):
        result = self.sample_controller.index()

        assert result
        assert isinstance(result, list)
        assert all([isinstance(obj, SampleModel) for obj in result])

    @pytest.mark.controller
    def test_save(self, setup):
        result = self.sample_controller.save(
            obj_data=self.sample_test_data.create_sample
        )

        assert result
        assert isinstance(result, SampleModel)
        assert self.db_instance.query(SampleModel).count() == 2

    @pytest.mark.controller
    def test_find(self, setup, caplog):
        result = self.sample_controller.find(obj_id=self.sample_model.id)

        assert result
        assert isinstance(result, SampleModel)
        with pytest.raises(AppException.BadRequest) as bad_request:
            self.sample_controller.find(obj_id=uuid.uuid4())
        assert bad_request.value.status_code == 400
        assert bad_request.value.error_message == "bad operation"
        assert len(caplog.messages) == 1

    @pytest.mark.controller
    def test_token(self, setup):
        result = self.sample_controller.token()

        assert result
        assert isinstance(result, dict)
