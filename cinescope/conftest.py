import pytest
import requests
from faker import Faker
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager

faker = Faker()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture
def user_for_tests(api_manager, test_user):
    """
    Создание и удаление уникального пользователя для каждого теста
    :param api_manager:
    :param test_user:
    :return:
    """
    user = api_manager.auth_api.register_user(test_user).json()
    yield test_user
    api_manager.auth_api.authenticate((test_user["email"], test_user["password"]))
    api_manager.user_api.delete_user(user["id"], expected_status=200)


@pytest.fixture
def clean_up_user(api_manager, test_user):
    yield
    api_manager.auth_api.authenticate((test_user["email"], test_user["password"]))
    api_manager.user_api.delete_user(test_user["id"], expected_status=200)
