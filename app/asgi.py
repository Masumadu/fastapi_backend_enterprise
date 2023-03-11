from app import create_app, constants
import os

config_env = os.getenv("FASTAPI_CONFIG")
assert config_env != constants.TESTING_ENVIRONMENT, constants.ENV_ERROR.format(config_env)
app = create_app()
