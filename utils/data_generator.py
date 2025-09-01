import random
import string
from faker import Faker

faker = Faker("ru_RU")


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_movie_data():
        return {
            "name": faker.sentence(nb_words=3),  # случайное название
            "imageUrl": faker.image_url(),  # случайная ссылка на картинку
            "price": random.randint(50, 500),  # цена от 50 до 500
            "description": faker.text(max_nb_chars=200),  # описание
            "location": random.choice(["SPB", "MSK"]),  # случайный город
            "published": faker.boolean(),  # True/False
            "genreId": random.randint(1, 5),  # случайный жанр (id от 1 до 5)
        }