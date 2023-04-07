class SampleTestData:
    @property
    def exiting_sample(self):
        return {
            "title": "sample_title",
            "content": "sample_content",
        }

    @property
    def create_sample(self):
        return {
            "title": "new_title",
            "content": "new_content",
        }

    @property
    def update_sample(self):
        return {
            "content": "updated_content",
        }
