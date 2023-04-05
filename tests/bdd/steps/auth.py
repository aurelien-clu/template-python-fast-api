from contextlib import suppress

from behave import step

from src import logger


@step("a logged test user")
def step_impl(context):
    path = "/auth/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    body = {"username": "test", "password": "secret"}

    response = context.client.post(path, headers=headers, data=body)
    check = response.status_code == 200
    if not check:
        with suppress(Exception):
            logger.error(response)
            logger.error(response.status_code)
            logger.error(response.content)
            logger.error(response.json())
    assert check
    context.token = response.json()
