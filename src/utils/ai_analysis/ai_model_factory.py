from src.utils.ai_analysis.ai_model import AiModel, MockAiModel, GeminiAiModel, EchoAiModel
from src.utils.settings import get_settings


class AiModelFactory:
    @staticmethod
    def create() -> AiModel:
        ai_model = get_settings().AI_MODEL

        if ai_model == 'mock':
            return MockAiModel()
        if ai_model == 'echo':
            return EchoAiModel()
        if ai_model == 'gemini':
            return GeminiAiModel()
        else:
            return MockAiModel()
