import pytest, os
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture()
def browser():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'download.prompt_for_download': False})
    options.add_experimental_option('prefs', {'disable-popup-blocking': False})
    options.add_experimental_option('prefs', {'download.directory_upgrade': True})
    #options.add_experimental_option('prefs', {'download.default_directory': dir_path})перестало работать
    options.add_experimental_option('prefs', {'safebrowsing.enabled': True})
    chrome_browser = webdriver.Chrome(options=options)
    chrome_browser.maximize_window()
    chrome_browser.implicitly_wait(10)
    return chrome_browser

