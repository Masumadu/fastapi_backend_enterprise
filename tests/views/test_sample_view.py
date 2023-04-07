import pytest

from tests.base_test_case import BaseTestCase


class TestSampleView(BaseTestCase):
    @pytest.mark.view
    def test_index(self, setup):
        response = setup.get("/prefix/get-all/")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, list)
        assert len(response_data) == 1

    @pytest.mark.view
    def test_find(self, setup):
        response = setup.get(f"/prefix/get/{self.sample_model.id}")
        response_data = response.json()

        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_create(self, setup):
        response = setup.post(
            "/prefix/create/", json=self.sample_test_data.create_sample
        )
        response_data = response.json()
        assert response.status_code == 201
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_token(self, setup):
        response = setup.post("/prefix/token/")
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)

    @pytest.mark.view
    def test_protected(self, setup):
        response = setup.post("/prefix/auth/", headers=self.headers)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data
        assert isinstance(response_data, dict)
