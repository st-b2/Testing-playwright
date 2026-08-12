import pytest
from playwright.sync_api import Page, expect


class TestAuthorizationNegative:
    """Негативные тесты авторизации пользователя"""

    # Негативные тесты - невалидные данные
    @pytest.mark.parametrize("username,password,expected_error", [
        ('', 'Password123', 'Пожалуйста, заполните все поля'),
        ('TestUser', '', 'Пожалуйста, заполните все поля'),
        ('', '', 'Пожалуйста, заполните все поля'),
        ('WrongUser', 'Password123', 'Неверный логин или пароль'),
        ('TestUser', 'WrongPass123', 'Неверный логин или пароль'),
        ('ab', 'Password123', 'Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _'),
        ('TestUser', 'Pass123', 'Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру'),
    ])
    def test_negative_invalid_login(self, page: Page, username, password, expected_error):
        """
        Негативный тест: попытка входа с невалидными данными
        """
        page.goto("https://intern.demoshopping.ru/")
        page.get_by_role("button", name="Регистрация / Войти").click()

        page.get_by_role("textbox", name="Login:").fill(username)
        page.get_by_role("textbox", name="Password:").fill(password)
        page.get_by_role("button", name="Войти").click()

        expect(page.get_by_text(expected_error)).to_be_visible()

    # Тест на проверку сообщения при ошибке сервера
    def test_server_error_handling(self, page: Page):
        """
        Тест обработки ошибки сервера
        """
        page.goto("https://intern.demoshopping.ru/")
        page.get_by_role("button", name="Регистрация / Войти").click()

        page.get_by_role("textbox", name="Login:").fill("TestUser123")
        page.get_by_role("textbox", name="Password:").fill("ValidPass123")

        page.get_by_role("button", name="Войти").click()

        try:
            expect(page.get_by_text("Произошла ошибка при обработке запроса")).to_be_visible(timeout=3000)
