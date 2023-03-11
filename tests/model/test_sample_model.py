import pytest
from app.models import SampleModel
from tests.base_test_case import BaseTestCase

class TestSampleModels(BaseTestCase):
    @pytest.mark.model
    def test_sample_model(self, setup):
        result = self.db_instance.query(SampleModel).get(self.sample_model.id)
        assert result
        assert hasattr(result, "id")
        assert hasattr(result, "title")
        assert hasattr(result, "content")
        assert result.id is not None
