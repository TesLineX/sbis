from page.page import Page
from selenium.webdriver.common.by import By
import requests as rq
import time
import os.path

link = 'https://sbis.ru/'
contact_selector = (By.LINK_TEXT, 'Контакты')
banner_selector = (By.CLASS_NAME, 'mb-12')
sila_selector = (By.XPATH, "//p[text()='Сила в людях']")
parent_sila_selector = (By.XPATH, "//p[text()='Сила в людях']/..")
images_selector = (By.XPATH, '//div[@class="tensor_ru-container tensor_ru-section tensor_ru-About__block3"]//img')
partners_selector = (By.XPATH, '//div[@class="sbisru-Contacts-List__col ws-flex-shrink-1 ws-flex-grow-1"]')
region_selector = (By.XPATH, '//span[@class="sbis_ru-Region-Chooser__text sbis_ru-link"]')
select_selector = (By.XPATH, '//span[text()="41 Камчатский край"]')
footer_selector = (By.LINK_TEXT, 'Скачать локальные версии')
plag_selector = (By.XPATH, '//div[text()="СБИС Плагин"]')
download_selector = (By.XPATH, '//a[@href="https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe"]')
#dir_path = os.path.dirname(os.path.realpath(__file__))

class SbisPage(Page):
    def __init__(self, browser):
        super().__init__(browser)

    def contacts(self):
        self.browser.get(link)
        link_contacts = self.find(contact_selector)
        link_contacts.click()
        link_banner = self.find(banner_selector)
        self.browser.get(link_banner.get_attribute('href'))
        self.find(sila_selector)
        sila_parent = self.find(parent_sila_selector)
        sila_parent = sila_parent.get_attribute('class')
        sila_link = self.browser.find_element(By.XPATH, f'//div[@class="{str(sila_parent)}"]//a[text()="Подробнее"]')
        sila_link = sila_link.get_attribute('href')
        self.browser.get(sila_link)
        images = self.finds(images_selector)
        width, height = [], []
        for image in images:
            width.append(image.size['width'])
            height.append(image.size['height'])
        assert 1 == len(set(width)), 'Ширина фото не совпадает'#сет хранит только уникальные значения
        assert 1 == len(set(height)), 'Высота фото не совпадает'
        self.browser.quit()

    def region(self):
        self.browser.get(link)
        link_contacts = self.find(contact_selector)
        link_contacts.click()
        partner = self.find(partners_selector)
        initial_list = self.find(partners_selector).text
        assert partner.is_displayed()
        ip = rq.get('https://checkip.amazonaws.com')
        ip = ip.text.strip()
        region = rq.get(f'https://api.2ip.me/geo.json?ip={ip}')
        region = region.json()
        region = region['region_rus'].split(' ')[0]
        region = region.split(' ')[0]
        region_on_site = self.find(region_selector).text
        assert region in region_on_site, f'Вычисленный регион - {region}, выбранный сайтом регион - {region_on_site}'
        self.find(region_selector).click()
        time.sleep(1)#явное ожидание для подгрузки элементов списка, без ожидания не срабатывает клик, implicitly_wait игнорируется
        new_region = self.find(select_selector).text
        self.find(select_selector).click()
        time.sleep(1)
        new_list = self.find(partners_selector).text
        assert self.find(region_selector).text in new_region, 'Подставленный регион не совпадает с выбранным'
        assert new_list not in initial_list, 'Список контактов не изменился'
        page_url_41 = self.browser.current_url
        assert '41-kamchatskij-kraj' in str(page_url_41), 'Выбранный регион в URL не указан'
        assert self.find(region_selector).text in self.browser.title, 'Выбранный регион в Title не указан'
        self.browser.quit()

    def download(self):
        self.browser.get(link)
        footer = self.find(footer_selector)
        self.browser.execute_script('arguments[0].click();', footer)
        time.sleep(2)
        plag_sbis = self.find(plag_selector)
        self.browser.execute_script('arguments[0].click();', plag_sbis)
        size_on_page = self.find(download_selector).text
        self.find(download_selector).click()
        usr_dir = os.path.expanduser("~")
        while os.path.lexists(f'{usr_dir}\\Downloads\\sbisplugin-setup-web.exe') is False:
            continue
        fsize = os.path.getsize(f'{usr_dir}\\Downloads\\sbisplugin-setup-web.exe')
        fsize = round(float(fsize / 1024 ** 2), 2)
        assert str(fsize) in size_on_page, f'Скачанный/заявленный объемы файла не совпадают: {fsize}МБ. <> {size_on_page}'
        self.browser.quit()
