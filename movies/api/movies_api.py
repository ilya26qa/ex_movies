from movies.constants import BASE_URL, MOVIES_URL
from movies.utils.custom_requester import CustomRequester


class MoviesApi(CustomRequester):
    """
    Класс для работы с MoviesApi.
    """
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def get_movies(self, params=None, expected_status=200):
        """
        Получение информации о пользователе.
        :param params: квери параметры для запроса
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_URL,
            params=params,
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        """
        Args:
            movie_data: тело для создания фильма
            expected_status: ожидаемый статус код

        Returns:
        ответ по запросу
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_URL,
            data=movie_data,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        """
        :param movie_id:
        :param expected_status:
        :return:
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_URL}/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        :param movie_id:
        :param expected_status:
        :return:
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_URL}/{movie_id}",
            expected_status=expected_status
        )

    def patch_movie(self, movie_id, patch_data, expected_status=200):
        """
        :param movie_id:
        :param patch_data:
        :param expected_status:
        :return:
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_URL}/{movie_id}",
            data=patch_data,
            expected_status=expected_status
        )
