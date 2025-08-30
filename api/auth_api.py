from constants import BASE_URL, AUTH_URL, LOGIN_ENDPOINT
from utils.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    """
    Класс для работы с аутентификацией.
    """
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, login_data):
        login_data = {
            "email": login_data[0],
            "password": login_data[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(self.session, authorization="Bearer " + token)

    def deauthenticate(self):
        self._update_session_headers(self.session, authorization=None)
