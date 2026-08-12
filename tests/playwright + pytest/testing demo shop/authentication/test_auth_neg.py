import pytest
from playwright.sync_api import Page, expect


class TestAuthorizationNegative:
    """Негативные тесты авторизации пользователя"""

    # Негативные тесты - невалидные данные
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
        page.goto("https://intern.demoshopping.ru/login")
        current_url = page.url

        page.get_by_role("textbox", name="Login:").fill(username)
        page.get_by_role("textbox", name="Password:").fill(password)
        page.get_by_role("button", name="Войти", exact=True).click()

        if expected_error is None:
            # Для пустых полей - проверяем, что мы остались на той же странице
            expect(page).to_have_url(current_url)
        else:
            # Для остальных случаев - проверяем сообщение об ошибке
            expect(page.get_by_text(expected_error)).to_be_visible()

    # Тест на проверку сообщения при ошибке сервера
    def test_server_error_handling(self, page: Page):
        """
        Тест обработки ошибки сервера
        """
        page.goto("https://intern.demoshopping.ru/login")
        page.get_by_role("textbox", name="Login:").fill("TestUser123")
        page.get_by_role("textbox", name="Password:").fill("ValidPass123")

        page.get_by_role("button", name="Войти", exact=True).click()

        expect(page.get_by_text("Произошла ошибка при обработке запроса")).to_be_visible(timeout=3000)
