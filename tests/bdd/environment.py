import warnings

from behave import fixture, use_fixture
from fastapi.testclient import TestClient

from src import logger
from src.app import create_app

warnings.simplefilter(action="ignore", category=FutureWarning)


@fixture
def feature_context(context):
    logger.info("creating feature context...")
    context.feature_context = {}
    yield
    logger.info("...destroying feature context")


@fixture
def api_client(context):
    logger.info("creating API client...")
    app = create_app()
    context.client = TestClient(app)
    yield
    logger.info("...destroying API client")


fixture_registry = {
    "fixture.feature.context": feature_context,
    "fixture.api.client": api_client,
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture(fixture_registry[tag], context)
