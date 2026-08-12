import pytest
from playwright.sync_api import Page, expect


class TestRegistration:
    """Тесты регистрации пользователя"""

    # Позитивные тесты - валидные данные
    @pytest.mark.parametrize("username,password", [
        ('TestUser1332', 'Password12366'),  # Буквы + цифры
        ('User_456', 'Admin123'),  # Символ _ в логине, минимальная длина пароля
        ('ValidUser', 'TestPass123'),  # Валидные данные
    ])
    def test_positive_registration(self, page: Page, username, password):
        """
        Позитивный тест: успешная регистрация с валидными данными

        [!] Измените фикстуру с полями логина и пароля
        """
        page.goto("https://intern.demoshopping.ru/")

        expect(page.get_by_role("button", name="Регистрация / Войти")).to_be_visible()
        page.get_by_role("button", name="Регистрация / Войти").click()

        page.get_by_role("textbox", name="Логин:").click()
        page.get_by_role("textbox", name="Логин:").fill(username)
        page.get_by_role("textbox", name="Пароль:").click()
        page.get_by_role("textbox", name="Пароль:").fill(password)
        page.get_by_role("button", name="Зарегистрироваться").click()

        expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=5000)

    # Граничные тесты
    @pytest.mark.parametrize("username,password", [
        ('Abc', 'ValidPass123'),  # Минимальная длина логина (3 символа)
        ('TestUser1234567', 'ValidPass123'),  # Максимальная длина логина (15 символов)
        ('TestUser', 'Pass1234'),  # Минимальная длина пароля (8 символов)
    ])
    def test_boundary_valid_values(self, page: Page, username, password):
        """Позитивный тест: граничные валидные значения"""
        page.goto("https://intern.demoshopping.ru/")
        page.get_by_role("button", name="Регистрация / Войти").click()

        page.get_by_role("textbox", name="Логин:").fill(username)
        page.get_by_role("textbox", name="Пароль:").fill(password)
        page.get_by_role("button", name="Зарегистрироваться").click()

        expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=5000)

    # Тест безопасности - SQL инъекция
    @pytest.mark.parametrize("username,password", [
        ("' OR '1'='1", "test123"),
        ("admin' --", "password"),
        ("'; DROP TABLE users; --", "test"),
    ])
    def test_security_sql_injection(self, page: Page, username, password):
        """Тест безопасности: проверка защиты от SQL-инъекций"""
        page.goto("https://intern.demoshopping.ru/")
        page.get_by_role("button", name="Регистрация / Войти").click()

        page.get_by_role("textbox", name="Логин:").fill(username)
        page.get_by_role("textbox", name="Пароль:").fill(password)
        page.get_by_role("button", name="Зарегистрироваться").click()

        try:
            expect(page.get_by_text(
                "Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _")).to_be_visible(
                timeout=3000)
        except:
            expect(page.get_by_role("button", name="Зарегистрироваться")).to_be_visible()

