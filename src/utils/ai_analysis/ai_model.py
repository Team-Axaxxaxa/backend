import abc

from openai.types.chat import ChatCompletionUserMessageParam

from src.utils.ai_analysis.client import get_client


class AiModel(abc.ABC):
    @abc.abstractmethod
    def analyse(self, data: str) -> str:
        pass


class MockAiModel(AiModel):
    def analyse(self, data: str) -> str:
        return "Mock"


class EchoAiModel(AiModel):
    def analyse(self, data: str) -> str:
        return data


class GeminiAiModel(AiModel):
    def analyse(self, data: str) -> str:
        client = get_client()
        char_completion = ChatCompletionUserMessageParam(
            role='user',
            content=data,
        )
        completion = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[char_completion]
        )
        return completion.choices[0].message.content
