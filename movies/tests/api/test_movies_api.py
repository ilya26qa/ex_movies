import pytest


class TestMoviesApi:
    def test_get_movies(self, api_manager):
        movies = api_manager.movies_api.get_movies()

        assert movies.json()['count'] > 0, "отсутствует количество фильмов"
        assert movies.json()['movies'] is not None, "список фильмов отсутствует"

    @pytest.mark.parametrize("published_params, expected_res", [
        ({"published": "false"}, False),
        ({"published": "true"}, True),
    ])
    def test_get_movies_with_published_filter(self, api_manager, published_params, expected_res):
        movies = api_manager.movies_api.get_movies(params=published_params)

        for movie in movies.json()['movies']:
            assert movie["published"] == expected_res

    def test_create_movie(self, api_manager, admin_auth, random_movie_data):
        movie_id = api_manager.movies_api.create_movie(random_movie_data).json()['id']
        movie = api_manager.movies_api.get_movie(movie_id)

        for i in random_movie_data:
            assert i in movie.json(), "данные с ответа не совпадают с переданными"

        api_manager.movies_api.delete_movie(movie_id)

    def test_create_movie_without_auth(self, api_manager, random_movie_data, deauthenticated):
        response = api_manager.movies_api.create_movie(random_movie_data, 401)

        assert response.json()['message'] == 'Unauthorized', 'в теле ответа нет надписи об отсутствии авторизации'

    def test_create_existing_movie(self, api_manager, admin_auth, random_movie_data):
        first_movie = api_manager.movies_api.create_movie(random_movie_data)
        second_movie = api_manager.movies_api.create_movie(random_movie_data, 409)
        api_manager.movies_api.delete_movie(first_movie.json()['id'])

        assert second_movie.json()['message'] == 'Фильм с таким названием уже существует', 'в теле ответа неправильная ошибка'

    def test_create_movie_without_name(self, api_manager, admin_auth, random_movie_data):
        del random_movie_data['name']
        movie = api_manager.movies_api.create_movie(random_movie_data, 400)

        assert 'name should not be empty' in movie.json()['message'], 'в теле ответа отсутствует ошибка'

    def test_get_existing_movie(self, api_manager, random_movie):
        movie = api_manager.movies_api.get_movie(random_movie['id'])

        assert movie.json()['name'], 'в отете отсутствует ID'
        assert movie.json()['id'], 'в ответе отсутствует название'

    def test_get_non_existing_movie(self, api_manager):
        movie = api_manager.movies_api.get_movie(0, expected_status=404)

        assert movie.json()['message'] == 'Фильм не найден', 'в теле ответа отсутствует ошибка'

    def test_delete_existing_movie(self, api_manager, admin_auth, random_movie_without_del):
        movie = api_manager.movies_api.delete_movie(random_movie_without_del.json()['id'])

        assert movie.json()['name'], 'в отете отсутствует ID'
        assert movie.json()['id'], 'в ответе отсутствует название'

    @pytest.mark.parametrize('value', [0,'dasdas'])
    def test_delete_non_existing_movie(self, api_manager, admin_auth, random_movie, value):
        movie = api_manager.movies_api.delete_movie(value, expected_status=404)

        assert movie.json()['message'] == 'Фильм не найден', 'в теле ответа отсутствует ошибка'

    def test_delete_movie_without_auth(self, api_manager, random_movie, deauthenticated):
        movie = api_manager.movies_api.delete_movie(random_movie['id'], 401)

        assert movie.json()['message'] == "Unauthorized", 'в теле нет ошибки авторизации'
        assert api_manager.movies_api.get_movie(random_movie['id']), 'удалено без аутентификации'

    def test_patch_movie(self, api_manager, admin_auth, random_movie, random_movie_data):
        patch_data = {k: random_movie_data[k] for k in ["name", "price"]}
        movie = api_manager.movies_api.patch_movie(random_movie['id'], patch_data)

        assert movie.json()['name'] == patch_data['name'], 'поле цены не изменилось'
        assert movie.json()['price'] == patch_data['price'], 'поле цены не изменилось'

        movie = api_manager.movies_api.get_movie(random_movie['id'])

        assert movie.json()['name'] == patch_data['name'], 'поле цены не изменилось'
        assert movie.json()['price'] == patch_data['price'], 'поле цены не изменилось'

    @pytest.mark.parametrize('value', [0, 'dasda'])
    def test_patch_nonexisting_movie(self, api_manager, admin_auth, random_movie_data, value):
        patch_data = {k: random_movie_data[k] for k in ["name", "price"]}
        movie = api_manager.movies_api.patch_movie(value, patch_data, 404)

        assert movie.json()['message'] == 'Фильм не найден'

    def test_patch_movie_invalid_data(self, api_manager, admin_auth, random_movie):
        movie = api_manager.movies_api.patch_movie(random_movie['id'], {'patch_data': "patch_data"}, 404)
        assert movie.json()['message'] == 'Фильм не найден'

        movie = api_manager.movies_api.get_movie(random_movie['id'])
        assert 'patch_data' not in movie.json()

    def test_patch_movie_without_auth(self, api_manager, admin_auth, random_movie, random_movie_data, deauthenticated):
        patch_data = {k: random_movie_data[k] for k in ["name", "price"]}
        movie = api_manager.movies_api.patch_movie(random_movie['id'], patch_data, 401)

        assert movie.json()['message'] == 'Unauthorized', 'в теле ответа нет надписи об отсутствии авторизации'
