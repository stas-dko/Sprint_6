from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.wait import WebDriverWait

WAIT_SECONDS = 5


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        '''Получение url текущей страницы.'''
        return self.driver.current_url

    def get_element(self, locator):
        '''Получение заданного элемента страницы.'''
        return self.driver.find_element(*locator)

    def wait_for(self, event, seconds=WAIT_SECONDS):
        '''Приостановка работы драйвера до наступления события.'''
        WebDriverWait(self.driver, seconds).until(event)

    def switch_window(self, url):
        '''Переключение на последнее открытое окно (вкладку) браузера.'''
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait_for(e_c.url_to_be(url))

    def scroll_to_element(self, locator):
        '''Прокрутка экрана до элемента.'''
        element = self.get_element(locator)
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)
        self.wait_for(e_c.visibility_of_element_located(locator))

    def click_element(self, locator):
        '''Клик по элементу с проверкой кликабельности и JS fallback.'''
        element = self.get_element(locator)
        self.scroll_to_element(locator)
        self.wait_for(e_c.element_to_be_clickable(locator))
        try:
            element.click()
        except:
            # Если Selenium жалуется, кликаем через JS
            self.driver.execute_script("arguments[0].click();", element)

    def fill_form_field(self, locator, *value):
        '''Заполнение поля формы.'''
        element = self.get_element(locator)
        self.scroll_to_element(locator)
        element.send_keys(*value)  # распаковываем кортеж значений