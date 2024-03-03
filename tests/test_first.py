from page.sbis import SbisPage

def test_contact(browser):
    sbis_page = SbisPage(browser)
    sbis_page.contacts()

def test_region(browser):
    sbis_page = SbisPage(browser)
    sbis_page.region()


def test_download(browser):
    sbis_page = SbisPage(browser)
    sbis_page.download()






