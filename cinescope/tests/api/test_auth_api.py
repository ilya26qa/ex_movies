from cinescope.api.api_manager import ApiManager


class TestAuthApi:
    def test_register_user(self, api_manager: ApiManager, test_user, clean_up_user):
        """
        Тест на регистрацию пользователя.
        """

        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        test_user['id'] = response_data['id']

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager: ApiManager, user_for_tests):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": user_for_tests["email"],
            "password": user_for_tests["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == user_for_tests["email"], "Email не совпадает"
