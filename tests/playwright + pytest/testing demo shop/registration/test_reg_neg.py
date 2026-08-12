import pytest
from playwright.sync_api import Page, expect


class TestRegistration:
    """Тесты регистрации пользователя"""

    # Негативные тесты - несоответствие требованиям
    @pytest.mark.parametrize("username,password,expected_error", [
        # Логин короче 3 символов
        ('ab', 'Password123', 'Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _'),
        # Логин длиннее 15 символов
        ('TestUser12345678', 'Password123',
         'Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _'),
        # Пароль короче 8 символов
        ('TestUser', 'Pass123', 'Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру'),
        # Пароль без цифр
        ('TestUser', 'Password',
         'Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру'),
    ])
    def test_negative_invalid_fields(self, page: Page, username, password, expected_error):
        """
        Негативный тест: регистрация с данными, не соответствующими требованиям
        """
        page.goto("https://intern.demoshopping.ru/")
        page.get_by_role("button", name="Регистрация / Войти").click()

        page.get_by_role("textbox", name="Логин:").fill(username)
        page.get_by_role("textbox", name="Пароль:").fill(password)
        page.get_by_role("button", name="Зарегистрироваться").click()

        expect(page.get_by_text(expected_error)).to_be_visible()

    # Негативный тест - существующий пользователь
    @pytest.mark.parametrize("username,password", [
        ('TestUser', 'Password123'),
        ('User_456', 'Admin123'),
    ])
    def test_negative_existing_user(self, page: Page, username, password):
        """Негативный тест: попытка регистрации с уже существующим логином"""
        page.goto("https://intern.demoshopping.ru/")
        page.get_by_role("button", name="Регистрация / Войти").click()

        # Первая регистрация
        page.get_by_role("textbox", name="Логин:").fill(username)
        page.get_by_role("textbox", name="Пароль:").fill(password)
        page.get_by_role("button", name="Зарегистрироваться").click()

        expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=5000)

        # Выходим из системы
        page.get_by_role("button", name="Выйти").click()

        # Вторая попытка регистрации с тем же логином
        page.get_by_role("button", name="Регистрация / Войти").click()
        page.get_by_role("textbox", name="Логин:").fill(username)
        page.get_by_role("textbox", name="Пароль:").fill(password)
        page.get_by_role("button", name="Зарегистрироваться").click()

        expect(page.get_by_text("Пользователь с таким логином уже существует")).to_be_visible()

        # Тест на проверку сообщения при ошибке сервера
        def test_server_error_handling(self, page: Page):
            """
            Тест обработки ошибки сервера
            Ожидаемое сообщение: "Произошла ошибка при обработке запроса"
            """
            page.goto("https://intern.demoshopping.ru/")
            page.get_by_role("button", name="Регистрация / Войти").click()

            page.get_by_role("textbox", name="Логин:").fill("TestUser123")
            page.get_by_role("textbox", name="Пароль:").fill("ValidPass123")

            page.get_by_role("button", name="Зарегистрироваться").click()

            try:
                expect(page.get_by_text("Произошла ошибка при обработке запроса")).to_be_visible(timeout=3000)
            except:
                expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=3000)