import json

from behave import step

from src import logger


@step("path: {path}")
def step_impl(context, path: str):
    context.request_path = path


@step("request headers: {new_header}")
def step_impl(context, new_header: str):
    headers = getattr(context, "request_headers", dict())
    merged_headers = {**headers, **json.loads(new_header)}
    context.request_headers = merged_headers


@step("bearer token in request headers")
def step_impl(context):
    headers = getattr(context, "request_headers", dict())
    headers["Authorization"] = f"Bearer {context.token['access_token']}"
    context.request_headers = headers


@step("request body: {body}")
def step_impl(context, body: str):
    request_body = json.loads(body)
    from_context = {}
    for key, value in request_body.items():
        if not isinstance(value, str):
            continue
        if value.lower() == "<from-context>":
            new_value = getattr(context, key)
            logger.debug(f"\t\tbody override from context: {key}: {new_value}")
            from_context[key] = new_value
        if value.lower() == "<from-feature-context>":
            new_value = context.feature_context[key]
            logger.debug(f"\t\tbody override from feature context: {key}: {new_value}")
            from_context[key] = new_value
    context.request_body = {**request_body, **from_context}


@step("posting data")
def step_impl(context):
    path = context.request_path
    headers = getattr(context, "request_headers", None)
    body = getattr(context, "request_body", None)
    response = context.client.post(path, headers=headers, data=body)
    context.response = response


@step("posting")
def step_impl(context):
    path = context.request_path
    headers = getattr(context, "request_headers", None)
    body = getattr(context, "request_body", None)
    logger.debug(f"path: {path}")
    logger.debug(f"headers: {headers}")
    logger.debug(f"body: {body}")
    response = context.client.post(path, headers=headers, json=body)
    context.response = response


@step("getting")
def step_impl(context):
    path = context.request_path
    headers = getattr(context, "request_headers", None)
    context.response = context.client.get(path, headers=headers)


@step("heading")
def step_impl(context):
    path = context.request_path
    headers = getattr(context, "request_headers", None)
    context.response = context.client.head(path, headers=headers)
