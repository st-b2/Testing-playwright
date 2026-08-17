import pytest
from playwright.sync_api import Page, expect
from pages.home_store_page import HomeStorePage
from pages.reg_and_login_page import LoginPage


class TestAuthorization:
    """Тесты авторизации пользователя"""

    # Позитивные тесты - успешный вход
    @pytest.mark.parametrize("username,password", [
        ('TestUser1332', 'Password12366'),
        ('User_456', 'Admin123'),
        ('ValidUser', 'TestPass123'),
    ])
    def test_positive_login(self, page: Page, username, password):
        """
        Позитивный тест: успешная авторизация с валидными данными
        """
        login_page = LoginPage(page)
        home_page = HomeStorePage(page)

        home_page.reg_or_login.click()

        login_page.login(username, password)

        expect(page).to_have_url("https://intern.demoshopping.ru/")
        home_page.logout_is_visible()

    # Граничные тесты
    @pytest.mark.parametrize("username,password", [
        ('Abc', 'ValidPass123'),              # Минимальная длина логина (3 символа)
        ('TestUser1234567', 'ValidPass123'),  # Максимальная длина логина (15 символов)
        ('TestUser', 'Pass1234'),             # Минимальная длина пароля (8 символов)
    ])
    def test_boundary_valid_values(self, page: Page, username, password):
        """
        Позитивный тест: граничные валидные значения

        [!] Тесты должны пройти, однако тесты с вводом ключей (логин:пароль) 1 и 3 не пройдут,
        так как в самом сайте ошибки сделаны намеренно (для локализации и тренинга)
        """
        home_page = HomeStorePage(page)
        login_page = LoginPage(page)

        home_page.reg_or_login.click()

        login_page.login(username, password)

        expect(page).to_have_url("https://intern.demoshopping.ru/")
        home_page.logout_is_visible()

    # Тест безопасности - SQL инъекция
    @pytest.mark.parametrize("username,password", [
        ("' OR '1'='1", "test123"),
        ("admin' --", "password"),
        ("'; DROP TABLE users; --", "test"),
    ])
    def test_security_sql_injection(self, page: Page, username, password):
        """
        Тест безопасности: проверка защиты от SQL-инъекций
        """
        login_page = LoginPage(page)
        home_page = HomeStorePage(page)

        home_page.reg_or_login.click()

        login_page.login(username, password)

        try:
            expect(page.get_by_text("Логин должен содержать от 3 до 15 символов "
                                    "и может включать буквы, цифры и символы: _ "
                                    "Пароль должен содержать не менее 8 символов, "
                                    "включая минимум одну букву и одну цифру")).to_be_visible(timeout=3000)
        except:
            expect(page.get_by_role("button", name="Войти", exact=True)).to_be_visible()