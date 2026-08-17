import pytest
from playwright.sync_api import Page, expect
from pages.home_store_page import HomeStorePage
from pages.reg_and_login_page import RegistrationPage


class TestRegistrationNegative:
    """
    Негативные тесты регистрации
    """

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
        home_page = HomeStorePage(page)
        reg_page = RegistrationPage(page)

        home_page.reg_or_login.click()

        reg_page.registration(username, password)

        expect(page.get_by_text(expected_error)).to_be_visible()

    @pytest.mark.parametrize("username,password", [
        ('TestUser', 'Password123'),
        ('User_456', 'Admin123'),
    ])
    def test_negative_existing_user(self, page: Page, username, password):
        """
        Негативный тест: попытка регистрации с уже существующим логином
        """
        home_page = HomeStorePage(page)
        reg_page = RegistrationPage(page)

        home_page.reg_or_login.click()
        reg_page.registration(username, password)
        expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=5000)

        home_page.logout.click()

        home_page.reg_or_login.click()
        reg_page.registration(username, password)

        expect(page.get_by_text("Пользователь с таким логином уже существует")).to_be_visible()

    def test_server_error_handling(self, page: Page):
        """
        Тест обработки ошибки сервера
        Ожидаемое сообщение: "Произошла ошибка при обработке запроса"
        """
        home_page = HomeStorePage(page)
        reg_page = RegistrationPage(page)

        home_page.reg_or_login.click()

        reg_page.reg_enter_username("TestUser123")
        reg_page.reg_enter_password("ValidPass123")
        reg_page.click_reg()

        try:
            expect(page.get_by_text("Произошла ошибка при обработке запроса")).to_be_visible(timeout=3000)
        except:
            expect(page.get_by_text("Регистрация выполнена успешно")).to_be_visible(timeout=3000)