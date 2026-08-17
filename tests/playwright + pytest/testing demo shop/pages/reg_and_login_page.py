from playwright.sync_api import Page

class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="Login:")
        self.password_input = page.get_by_role("textbox", name="Password:")


    def enter_username(self, username: str):
        self.username_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.page.get_by_role("button", name="Войти", exact=True).click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

class RegistrationPage:

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="Логин:")
        self.password_input = page.get_by_role("textbox", name="Пароль:")

    def reg_enter_username(self, username: str):
        self.username_input.fill(username)

    def reg_enter_password(self, password: str):
        self.password_input.fill(password)

    def click_reg(self):
        self.page.get_by_role("button", name="Зарегистрироваться").click()

    def registration(self, username: str, password: str):
        self.reg_enter_username(username)
        self.reg_enter_password(password)
        self.click_reg()