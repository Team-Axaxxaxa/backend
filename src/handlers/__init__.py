from src.handlers.health_check import api_router as health_router
from src.handlers.create_answer import api_router as create_answer_router
from src.handlers.create_test_taker import api_router as create_test_taker_router
from src.handlers.get_answer import api_router as get_answer_router
from src.handlers.get_question import api_router as get_question_router
from src.handlers.get_random_unfilled_question import api_router as get_random_unfilled_question_router

list_of_routes = [
    health_router,
    create_answer_router,
    create_test_taker_router,
    get_answer_router,
    get_question_router,
    get_random_unfilled_question_router,
]

__all__ = [
    'list_of_routes',
]