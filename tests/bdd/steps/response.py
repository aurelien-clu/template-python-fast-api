from contextlib import suppress
from datetime import datetime
from pathlib import Path

from behave import step

from src import logger


@step("response code is {code}")
def step_impl(context, code: str):
    check = context.response.status_code == int(code)
    if not check:
        with suppress(Exception):
            logger.error(context.response)
            logger.error(context.response.status_code)
            logger.error(context.response.content)
            logger.error(context.response.json())

    assert check


@step('json response is "{text}"')
def step_impl(context, text: str):
    check = context.response.json() == text
    if not check:
        with suppress(Exception):
            logger.error(context.response.json())
    assert check


@step("json response contains a non-null {key}")
def step_impl(context, key: str):
    check = context.response.json().get(key) is not None
    if not check:
        with suppress(Exception):
            logger.error(context.response.json())
    assert check


@step("json response contains {key} with a length in [{min_}, {max_}]")
def step_impl(context, key: str, min_, max_):
    value = context.response.json().get(key)
    check = int(min_) <= len(value) <= int(max_)
    if not check:
        with suppress(Exception):
            for _ in range(3):  # behave covers some logs
                logger.error(f"key.length={len(value)}")

    assert check


@step("adding {key} from the json response to the feature context as {name}")
def step_impl(context, key, name):
    value = context.response.json().get(key)
    context.feature_context[name] = value


@step("save json response {key} to {path}")
def step_impl(context, key, path):
    value = context.response.json().get(key)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(value)
