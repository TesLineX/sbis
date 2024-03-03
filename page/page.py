class Page:
    def __init__(self, browser):
        self.browser = browser

    def find(self, args):
        return self.browser.find_element(*args)

    def finds(self, args):
        return self.browser.find_elements(*args)
