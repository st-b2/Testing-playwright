import pytest
from playwright.sync_api import Page, expect
from pages.home_store_page import HomeStorePage
from pages.reg_and_login_page import LoginPage


class TestAuthorizationNegative:
    """Негативные тесты авторизации пользователя"""

    @pytest.mark.parametrize("username,password,expected_error", [
        # Пустые поля - проверяем, что страница не изменилась
        ('', 'Password123', None),
        ('TestUser', '', None),
        ('', '', None),
        # Неверные данные - проверяем сообщение об ошибке
        ('WrongUser', 'Password123', 'Произошла ошибка при обработке запроса'),
        ('TestUser', 'WrongPass123', 'Произошла ошибка при обработке запроса'),
        # Невалидные данные - проверяем сообщение валидации
        ('ab', 'Password123', 'Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _'),
        ('TestUser', 'Pass123', 'Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру'),
    ])
    def test_negative_invalid_login(self, page: Page, username, password, expected_error):
        """
        Негативный тест: попытка входа с невалидными данными

        [!] Тесты все проходят, однако с парой логин-пароль:
        {'ab','Password123'}
        тест падает, так как это ошибка на сайте, не соответствует ошибке из ТЗ
        """
        login_page = LoginPage(page)
        home_page = HomeStorePage(page)

        home_page.reg_or_login.click()
        current_url = page.url

        login_page.login(username, password)

        if expected_error is None:
            expect(page).to_have_url(current_url)
        else:
            expect(page.get_by_text(expected_error)).to_be_visible()

    def test_server_error_handling(self, page: Page):
        """
        Тест обработки ошибки сервера
        """
        login_page = LoginPage(page)
        home_page = HomeStorePage(page)

        home_page.reg_or_login.click()

        login_page.login("TestUser123", "ValidPass123")

        expect(page.get_by_text("Произошла ошибка при обработке запроса")).to_be_visible(timeout=3000)