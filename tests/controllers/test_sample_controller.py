import uuid
from unittest import mock

import pytest

from app.core.exceptions import AppException
from app.enums import TokenTypeEnum
from app.models import SampleModel
from tests.base_test_case import BaseTestCase


class TestSampleController(BaseTestCase):
    @pytest.mark.controller
    def test_get_resource(self, test_app, caplog):
        result = self.sample_controller.get_resource(query_params={})

        assert result
        assert isinstance(result, list)
        assert all([isinstance(obj, SampleModel) for obj in result])
        with pytest.raises(AppException.NotFoundException) as not_found:
            self.sample_controller.get_resource(
                query_params={"resource_id": uuid.uuid4()}
            )
        assert not_found.value.status_code == 404
        assert "does not exist" in not_found.value.error_message
        assert len(caplog.messages) == 1

    @pytest.mark.controller
    def test_create_resource(self, test_app):
        result = self.sample_controller.create_resource(
            obj_data=self.sample_test_data.create_sample
        )

        assert result
        assert isinstance(result, SampleModel)
        assert self.db_instance.query(SampleModel).count() == 2

    @pytest.mark.controller
    def test_update_resource(self, test_app):
        result = self.sample_controller.update_resource(
            obj_id=self.sample_model.id, obj_data=self.sample_test_data.update_sample
        )

        assert result
        assert isinstance(result, SampleModel)
        assert result.content == self.sample_test_data.update_sample.get("content")

    @pytest.mark.controller
    def test_delete_resource(self, test_app):
        result = self.sample_controller.delete(obj_id=self.sample_model.id)

        assert result is None

    @pytest.mark.controller
    def test_get_token(self, test_app):
        result = self.sample_controller.get_token()

        assert result
        assert isinstance(result, dict)

    @pytest.mark.controller
    @mock.patch("app.utils.auth.jwt.decode")
    def test_refresh_token(self, mock_jwt_decode, test_app):
        mock_jwt_decode.return_value = self.mock_decode_token(
            TokenTypeEnum.refresh_token.value
        )
        result = self.sample_controller.refresh_token(
            obj_data={"refresh_token": self.refresh_token}
        )

        assert result
        assert isinstance(result, dict)
