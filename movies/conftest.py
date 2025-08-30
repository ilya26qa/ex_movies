import os
import pytest
import requests
from dotenv import load_dotenv
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from api.auth_api import AuthAPI

load_dotenv()


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


@pytest.fixture(scope="session")
def admin_auth(api_manager):
    api_manager.auth_api.authenticate((os.environ.get("admin_login"), os.environ.get("admin_password")))


@pytest.fixture
def deauthenticated(api_manager):
    yield api_manager.auth_api.deauthenticate()
    api_manager.auth_api.authenticate((os.environ.get("admin_login"), os.environ.get("admin_password")))


@pytest.fixture
def random_movie_data(api_manager):
    return DataGenerator.generate_random_movie_data()


@pytest.fixture
def random_movie(api_manager, admin_auth, random_movie_data):
    movie = api_manager.movies_api.create_movie(random_movie_data)
    yield movie.json()
    api_manager.movies_api.delete_movie(movie.json()["id"])


@pytest.fixture
def random_movie_without_del(api_manager, admin_auth, random_movie_data):
    return api_manager.movies_api.create_movie(random_movie_data)
