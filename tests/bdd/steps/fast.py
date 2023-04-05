from behave import step
from fastapi.testclient import TestClient

from src.app import create_app


@step("an API client")
def step_impl(context):
    app = create_app()
    context.client = TestClient(app)
