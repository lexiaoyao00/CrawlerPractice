from playwright.sync_api import sync_playwright



class ChromeDriver():
    def  __init__(self,url=None,headless=False):
        self.url = url
        self.headless = headless

        self.page = None
    
    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.goto(self.url)

        return self.page


    def click(self,selector:str,**kwargs):
        self.page.locator(selector,**kwargs).click()

    def fill(self,selector:str,value:str,**kwargs):
        self.page.locator(selector,**kwargs).fill(value)


    def stop(self):
        self.browser.close()
        self.playwright.stop()


    def __del__(self):
        self.stop()