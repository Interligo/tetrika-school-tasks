import json

import requests
from requests.exceptions import InvalidURL
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as bs
from selenium import webdriver


class WikiCrawler:
    """
============================================================
Класс предназначен для поиска наименований животных на Wiki.
============================================================
    """
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.190 Safari/537.36'
        }
        self.wiki_url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:' \
                        '%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0' \
                        '%D0%B2%D0%B8%D1%82%D1%83'
        self.current_url = ''
        self.browser = webdriver.Chrome()
        self.result = dict()
        self.additional_result_info = dict()
        self.file_to_save_result = 'task2_animals_list.json'
        self.russian_alphabet = True

    def __str__(self):
        return 'Парсер страницы Вики животных по алфавиту'

    def __repr__(self):
        return 'Парсер страницы Вики животных по алфавиту'

    def _clear_result_before_save(self) -> None:
        """Служебная функция очищает результат от лишних данных, которые туда попали до остановки парсинга."""
        for symbol in ['A', 'H']:
            try:
                del self.result[symbol]
                del self.additional_result_info[symbol]
            except KeyError:
                pass

    def _check_russian_alphabet(self, first_symbol: str) -> None:
        """Служебная функция проверяет когда следует завершить парсинг, поскольку начался английский алфавит."""
        if first_symbol == 'A':  # Английская буква 'A'
            self.russian_alphabet = False

    def save_result_to_json(self) -> None:
        """Функция сохраняет дополнительные данные о результате в формате JSON."""
        with open(self.file_to_save_result, 'w', encoding='utf-8') as file:
            json.dump(self.additional_result_info, file, sort_keys=True, indent=4, ensure_ascii=False)

    def count_animal_name(self, animal_name: str) -> None:
        """
        Функция ведет подсчет количества имен животных на каждую букву русского алфавита.
        Дополнительно сохраняет перечень имен для последующего сохранения в JSON-файл.
        """
        first_symbol = animal_name[:1].capitalize()
        self._check_russian_alphabet(first_symbol)

        if first_symbol in self.result:
            self.result[first_symbol] += 1
            self.additional_result_info[first_symbol].append(animal_name)
        else:
            self.result[first_symbol] = 1
            self.additional_result_info[first_symbol] = [animal_name]

    def click_button_to_get_next_page(self, url_to_click: str) -> str:
        """
        Функция ищет кнопку переключения на следующую страницу wiki, нажимает на неё, переходит на следующую страницу
        и сохраняет свой текущий URL для последующего парсинга.
        """
        self.browser.get(url_to_click)
        next_page = self.browser.find_element_by_link_text('Следующая страница')
        next_page.click()
        next_url = self.browser.current_url
        return next_url

    def parse_page(self, url_to_parse: str) -> None:
        """Функция парсит список животных с переданной ей ссылки."""
        try:
            response = self.session.get(url_to_parse, headers=self.headers)

            if response.status_code == 200:
                soup = bs(response.content, 'lxml')
                all_li_tags = soup.find_all('li')

                for li in all_li_tags:
                    content_in_li = li.find('a')

                    try:
                        animal_name = content_in_li['title']
                        if animal_name == 'Категория:Животные':
                            break
                        elif animal_name in [
                            'Категория:Знаменитые животные по алфавиту',
                            'Категория:Породы собак по алфавиту'
                        ]:
                            continue

                        self.count_animal_name(animal_name)
                    except (TypeError, KeyError):
                        pass

        except (InvalidURL, ConnectionError):
            pass

    def parse_all_pages(self) -> dict:
        """Главная функция для парсинга всех страниц списка животных на русском."""
        self.parse_page(self.wiki_url)
        self.current_url = self.wiki_url

        while self.russian_alphabet:
            self.current_url = self.click_button_to_get_next_page(self.current_url)
            self.parse_page(self.current_url)

        self._clear_result_before_save()
        self.save_result_to_json()
        self.browser.quit()
        return self.result


if __name__ == '__main__':
    parser = WikiCrawler()
    result = parser.parse_all_pages()

    for key, value in result.items():
        print(f'{key}: {value}')
