from api.auth_api import AuthAPI
from api.movies_api import MoviesApi


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.movies_api = MoviesApi(session)
        self.auth_api = AuthAPI(session)
