'''Тесты главной страницы web-сервиса «Яндекс.Самокат».'''
import allure
import pytest

from data import FAQ
from pages.main_page import MainPage


class TestMainPage:
    @allure.title('Корректное отображение ответа на вопрос')
    @pytest.mark.parametrize('num', FAQ)
    def test_click_on_question_shows_answer(self, driver, num):
        '''По клику на кнопку-вопрос отображается корректный ответ.'''
        main_page = MainPage(driver)
        assert main_page.get_question_text(num) == FAQ[num]['q']
        assert not main_page.check_answer_field_is_shown(num)
        main_page.question_click(num)
        assert main_page.check_answer_field_is_shown(num)
        assert main_page.get_answer_text(num) == FAQ[num]['a']
