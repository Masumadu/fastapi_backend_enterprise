from unittest import mock

import pytest

from app.enums import TokenTypeEnum
from tests.base_test_case import BaseTestCase

BASE_URL = "/api/v1/sample-resource"


class TestSampleView(BaseTestCase):
    @pytest.mark.view
    def test_get_resource(self, test_app):
        response = test_app.get(
            f"{BASE_URL}/", params={"resource_id": self.sample_model.id}
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_create_resource(self, test_app):
        response = test_app.post(
            f"{BASE_URL}/", json=self.sample_test_data.create_sample
        )
        response_data = response.json()
        assert response.status_code == 201
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_update_resource(self, test_app):
        response = test_app.patch(
            f"{BASE_URL}/{self.sample_model.id}",
            json=self.sample_test_data.update_sample,
            headers=self.headers,
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_delete_resource(self, test_app):
        response = test_app.delete(
            f"{BASE_URL}/{self.sample_model.id}", headers=self.headers
        )
        assert response.status_code == 204

    @pytest.mark.view
    def test_get_token(self, test_app):
        response = test_app.get(f"{BASE_URL}/get-token/")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    @mock.patch("app.utils.auth.jwt.decode")
    def test_fresh_token(self, mock_decode_token, test_app):
        mock_decode_token.return_value = self.mock_decode_token(
            TokenTypeEnum.refresh_token.value
        )
        response = test_app.post(
            f"{BASE_URL}/refresh-token/", json={"refresh_token": self.refresh_token}
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)
