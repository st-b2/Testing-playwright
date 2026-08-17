from playwright.sync_api import Page, expect


class HomeStorePage:

    def __init__(self, page: Page):
        self.page = page
        self.logout = page.locator("#logout-button")
        self.catalog = page.get_by_role("link", name="Каталог")
        self.about_company = page.get_by_role("link", name="О компании")
        self.contacts = page.get_by_role("link", name="Контакты")
        self.cart = page.get_by_role("textbox", name="Корзина")
        self.payment = page.get_by_role("link", name="Оплата")
        self.history = page.get_by_role("link", name="История заказов")
        self.reg_or_login = page.locator("#login-button")

    def click_login_button(self):
        """Клик по кнопке 'Регистрация / Войти'"""
        self.reg_or_login.click()

    def click_logout(self):
        """Клик по кнопке 'Выйти'"""
        self.logout.click()

    def logout_is_visible(self):
        """Проверка видимости кнопки 'Выйти'"""
        expect(self.logout).to_be_visible()

    def go_to_catalog(self):
        """Переход в каталог"""
        self.catalog.click()

    def go_to_about(self):
        """Переход на страницу 'О компании'"""
        self.about_company.click()

    def go_to_contacts(self):
        """Переход на страницу 'Контакты'"""
        self.contacts.click()

    def go_to_payment(self):
        """Переход на страницу 'Оплата'"""
        self.payment.click()

    def go_to_history(self):
        """Переход в историю заказов"""
        self.history.click()