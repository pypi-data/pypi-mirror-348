import os
import base64

import nest_asyncio
import logfire

def load_config():
    os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-1f8f7293-bfa6-4293-9715-92a21f640ac3"
    os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-ed2096e3-5b22-4f5f-b8e5-359a3b07c184"
    os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com"

    LANGFUSE_AUTH = base64.b64encode(
        f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
    ).decode()

    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = os.environ.get("LANGFUSE_HOST") + "/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

    nest_asyncio.apply()

    logfire.configure(
        service_name='ci_agent',
        send_to_logfire=False,
    )


def get_trace_url(user_id: str) -> str:
    host = os.environ.get("LANGFUSE_HOST")
    return f"{host}/project/cmaoxupai007gad07qlvsutd6/users/{user_id}"


def get_user_id() -> str:
    return os.environ.get("LANGFUSE_USER_ID", "rc")
