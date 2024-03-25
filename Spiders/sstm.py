from Spiders import *
import time

class SSTM():
    def __init__(self,url:str):
        self.driver = ChromeDriver(url = url,headless=False)
        self.page = self.driver.start()

    def login(self,username:str,password:str):
        try:
            self.driver.click("#elSignInLink")

            self.driver.fill('input[type="email"]',username)
            self.driver.fill('input[type="password"]',password)

            self.driver.click('button[type="submit"][name="_processLogin"]')

        except Exception as e:
            print("Error:",e)

    def signIn(self):
        try:
            self.driver.click('#elNavigation_43')

            # self.driver.click('li.ipsMenu_item a[href*="/forum/72"]') #TODO 定位还需要再确认看看

            self.driver.page.get_by_role("link", name="我要签到【热门】").click()

            self.driver.click('//ol[@data-role="tableRows"]/li[1]/div[@class="ipsDataItem_main"]/h4/span[2]/a') #TODO XPATH选择 后面还需确认看看


            message = time.strftime("%Y%m%d", time.localtime())
            self.__reply(message)

        except Exception as e:
            print("Error:",e)

    def __reply(self, message):
        try:
            self.driver.click('a[data-action="replyToTopic"]')
            time.sleep(1)
            self.driver.click('#comments > div.cTopicPostArea.ipsBox.ipsResponsive_pull.ipsPadding.ipsSpacer_top > form > div > div.ipsComposeArea_editor > div.ipsType_normal.ipsType_richText.ipsType_break > div:nth-child(1) > div.ipsComposeArea_dummy.ipsJS_show')

            self.driver.fill('#cke_1_contents > div',message)

            # self.driver.click('button.ipsButton.ipsButton_primary')

#cke_1_contents > div

        except Exception as e:
            print("Error:",e)

    def __del__(self):
        self.driver.stop()


def mainProcess():
    sstm = SSTM(sstm_url)
    sstm.login("2950848462@qq.com","xc1290435868+")
    sstm.signIn()



    time.sleep(10)
