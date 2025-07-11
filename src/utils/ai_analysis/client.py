from openai import OpenAI

from src.utils.settings import get_settings


def get_client() -> OpenAI:
    client = OpenAI(
        base_url='https://openrouter.ai/api/v1',
        api_key=get_settings().OPEN_ROUTER_API_KEY,
    )
    return client
