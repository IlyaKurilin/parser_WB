import time
import pandas as pd
from lorem_text import lorem
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright


class WB:
    def __init__(self, search_name: str):
        self.search_name = search_name

    def get_link_for_parse(self, sort_="По рейтингу"):
        """Вытаскиваем ссылку нужной страницы через поиск ВБ с сортировкой по рейтингу"""
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel="chrome", headless=False)
            page = browser.new_page()
            page.goto('https://www.wildberries.ru/')
            time.sleep(3)
            page.locator('#searchInput').fill(self.search_name)
            page.keyboard.press('Enter')
            page.get_by_text("По популярности", exact=True).click()
            page.get_by_text(f'{sort_}', exact=True).click()
            time.sleep(5)
            self.link = page.content()

    def get_result(self):
        """Забираем данные с html"""
        html = bs(self.link, "html.parser")
        search = html.findAll('a', class_="product-card__link")
        prices = html.findAll('ins', class_="price__lower-price")
        rating = html.findAll('span', class_="address-rate-mini address-rate-mini--sm")
        marks = html.findAll('span', class_="product-card__count")
        time.sleep(6)
        self.data = {"Ссылка на товар": [link.get('href') for link in search],
                     "Наименование товара": [name.get('aria-label') for name in search],
                     "Цена товара": [price.text.strip(' ') for price in prices],
                     "Рейтинг товара": [float(rang.text) for rang in rating],
                     "Количество оценок у товара": [mark.text for mark in marks]}

    def generate_xlsx(self):
        """Генерим таблицу в xlsx"""
        df = pd.DataFrame(self.data)
        name_xlsx = lorem.words(1)
        time.sleep(5)
        df.to_excel(f'{name_xlsx}.xlsx', index=False)

    def full_script_example(self):
        """Собираем скрипт"""
        self.get_link_for_parse()
        self.get_result()
        self.generate_xlsx()


if __name__ == '__main__':
    WB(input("Введи то что будешь искать на WB: ")).full_script_example()
