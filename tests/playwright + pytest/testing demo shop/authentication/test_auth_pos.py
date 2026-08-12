import pytest
from playwright.sync_api import Page, expect


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
        page.goto("https://intern.demoshopping.ru/login")

        page.get_by_role("textbox", name="Login:").click()
        page.get_by_role("textbox", name="Login:").fill(username)
        page.get_by_role("textbox", name="Password:").click()
        page.get_by_role("textbox", name="Password:").fill(password)
        page.get_by_role("button", name="Войти", exact=True).click()

        # Проверяем редирект на главную страницу
        expect(page).to_have_url("https://intern.demoshopping.ru/")

        # Проверяем, что кнопка сменилась на "Выйти"
        expect(page.get_by_role("button", name="Выйти")).to_be_visible(timeout=5000)

    # Граничные тесты
    @pytest.mark.parametrize("username,password", [
        ('Abc', 'ValidPass123'),              # Минимальная длина логина (3 символа)
        ('TestUser1234567', 'ValidPass123'),  # Максимальная длина логина (15 символов)
        ('TestUser', 'Pass1234'),             # Минимальная длина пароля (8 символов)
    ])
    def test_boundary_valid_values(self, page: Page, username, password):
        """Позитивный тест: граничные валидные значения

        [!] Тесты должны пройти, однако тесты с вводом ключей (логин:пароль) 1 и 3 не пройдут,
        так как в самом сайте ошибки сделаны намеренно (для локализации и тренинга)

        """
        page.goto("https://intern.demoshopping.ru/")
        page.get_by_role("button", name="Регистрация / Войти").click()

        page.get_by_role("textbox", name="Login:").fill(username)
        page.get_by_role("textbox", name="Password:").fill(password)
        page.get_by_role("button", name="Войти").click()

        # Проверяем редирект на главную страницу
        expect(page).to_have_url("https://intern.demoshopping.ru/")

        expect(page.get_by_role("button", name="Выйти")).to_be_visible()

    # Тест безопасности - SQL инъекция
    @pytest.mark.parametrize("username,password", [
        ("' OR '1'='1", "test123"),
        ("admin' --", "password"),
        ("'; DROP TABLE users; --", "test"),
    ])
    def test_security_sql_injection(self, page: Page, username, password):
        """Тест безопасности: проверка защиты от SQL-инъекци"""
        page.goto("https://intern.demoshopping.ru/login")

        page.get_by_role("textbox", name="Login:").fill(username)
        page.get_by_role("textbox", name="Password:").fill(password)
        page.get_by_role("button", name="Войти", exact=True).click()

        try:
            (expect(page.get_by_text("Логин должен содержать от 3 до 15 символов "
                                     "и может включать буквы, цифры и символы: _ "
                                    "Пароль должен содержать не менее 8 символов, "
                                     "включая минимум одну букву и одну цифру")).
             to_be_visible(timeout=3000))
        except:
            expect(page.get_by_role("button", name="Войти", exact=True)).to_be_visible()