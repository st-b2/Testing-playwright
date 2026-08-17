import pytest
from playwright.sync_api import Page, expect
from pages.home_store_page import HomeStorePage
from pages.reg_and_login_page import RegistrationPage


class TestRegistration:
    """Тесты регистрации пользователя"""

    @pytest.mark.parametrize("username,password", [
        ('TestUser1332', 'Password12366'),  # Буквы + цифры
        ('User_456', 'Admin123'),  # Символ _ в логине, минимальная длина пароля
        ('ValidUser', 'TestPass123'),  # Валидные данные
    ])
    def test_positive_registration(self, page: Page, username, password):
        """
        Позитивный тест: успешная регистрация с валидными данными
        """
        home_page = HomeStorePage(page)
        reg_page = RegistrationPage(page)

        home_page.reg_or_login.click()

        reg_page.registration(username, password)

        expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=5000)

    # Граничные тесты
    @pytest.mark.parametrize("username,password", [
        ('Abc', 'ValidPass123'),  # Минимальная длина логина (3 символа)
        ('TestUser1234567', 'ValidPass123'),  # Максимальная длина логина (15 символов)
        ('TestUser', 'Pass1234'),  # Минимальная длина пароля (8 символов)
    ])
    def test_boundary_valid_values(self, page: Page, username, password):
        """
        Позитивный тест: граничные валидные значения
        """
        home_page = HomeStorePage(page)
        reg_page = RegistrationPage(page)

        home_page.reg_or_login.click()

        reg_page.registration(username, password)

        expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=5000)

    @pytest.mark.parametrize("username,password", [
        ("' OR '1'='1", "test123"),
        ("admin' --", "password"),
        ("'; DROP TABLE users; --", "test"),
    ])
    def test_security_sql_injection(self, page: Page, username, password):
        """
        Тест безопасности: проверка защиты от SQL-инъекций
        """
        home_page = HomeStorePage(page)
        reg_page = RegistrationPage(page)

        home_page.reg_or_login.click()

        reg_page.reg_enter_username(username)
        reg_page.reg_enter_password(password)
        reg_page.click_reg()

        try:
            expect(page.get_by_text(
                "Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _")).to_be_visible(
                timeout=3000)
        except:
            expect(page.get_by_role("button", name="Зарегистрироваться")).to_be_visible()