import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import openpyxl as op
import configparser
import os
import chromedriver_autoinstaller
from selenium import webdriver



class FBcrawl:

    def __init__(self, driver,account, password,amount):
        self.driver=driver
        self.account = account
        self.password = password
        self.FB_url = "https://www.facebook.com/"
        self.xlsxPath ='test.xlsx'
        self.webaddress_url ="data/webaddress.txt"
        self.Amount=amount

       #login FB use account.ini
    def login(self):
        driver.maximize_window()
        driver.get(self.FB_url)
        time.sleep(3)
        try:
            print("login")
            inputemail = driver.find_element(By.NAME,"email")
            inputemail.send_keys(self.account)
            intputpass = driver.find_element(By.NAME,"pass")
            intputpass.send_keys(self.password)
            button= driver.find_element(By.NAME,"login")
            button.click()
        except:
            print("login error")
        finally:
            print("login success")
        

    def setting(self):
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("prefs", {"profile.peeasf_manager_enabled": False, "credentials_enable_service": False})
            options.add_argument("--disable-infobars")
            options.add_argument("start-maximized")
            options.add_argument("--disable-extensions")
            options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
            return options

        #goto diff page use write() to load data
    def mult_web(self):
        f=open(self.webaddress_url,"r")
        webaddress=f.readlines()
        for i in range(len(webaddress)):
            print(webaddress[i][:-1])
            self.write(webaddress[i][:-1],'工作表'+str(i+1))
            time.sleep(2)
        f.close()
        self.driver.close()
        
        #load data and write to excel
    def load_xlsx(self,worksheet):
        wb = op.load_workbook(self.xlsxPath)
        sheet = wb[worksheet]
        last=sheet["A3"]
        wb.close
        return last.value




    def write(self,address,worksheet):
        time.sleep(2)
        self.driver.get(address)
        wb = op.load_workbook(self.xlsxPath)
        time.sleep(3)
        sheet = wb[worksheet]
        max=self.load_xlsx(worksheet)
        
        while True:
            firstcheck=driver.execute_script("return document.body.scrollHeight;")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            Seccheck=driver.execute_script("return document.body.scrollHeight;")
            if(firstcheck==Seccheck):
                break
            time.sleep(3)

        load_all_data(driver,sheet)
        print("Successful")
        wb.save('test.xlsx')

def load_all_data(driver,sheet):
        listrow=["B1","B","C1","C","D1","D","E1","E","F1","F"]
        soup=BeautifulSoup(driver.page_source,'html.parser')
        title=soup.title
        print(title.string)
        b=soup.findChildren("div",class_="xamitd3 x1sy10c2 xieb3on x193iq5w xrljuej x1aody8q")
        a=soup.find_all("div",class_="x1jx94hy x30kzoy x9jhf4c xgqcy7u x1lq5wgf xev17xk xktsk01 x1d52u69 x19i0xim x6ikm8r x10wlt62 x1n2onr6")#x1y1aw1k x1pi30zi x18d9i69 x1swvt13
        #print(a)

        #檢查重複依據
        checkpoint=[sheet["A2"].value,sheet["A3"].value,sheet["A4"].value,sheet["A5"].value]
        print(len(a))

        #從第二格開始存
        num=2

        #開始加人
        for i in a:
            Name=i.find_all("span",class_="xt0psk2")
            Name1=Name[0].find("a",class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv x1s688f")
            QA=i.find_all("li",class_="x1y1aw1k x4uap5 xwib8y2 xkhd6sd")
            print(Name1.string)
            count=0
            if(checkpoint[0]==Name1.string or checkpoint[1]==Name1.string or checkpoint[2]==Name1.string or checkpoint[3]==Name1.string):
                break
            sheet.insert_rows(num)
            for k in range(len(QA)):
                b=QA[k].find("span",class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f x12scifz")
                c=QA[k].find("span",class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u")
                sheet["A"+str(num)].value=Name1.string
                print(b.string)
                print(c.string)
                for i in range(0,len(listrow)-1,2):
                    if(sheet[listrow[i]].value==b.string):
                        sheet[listrow[i+1]+str(num)].value=c.string
            num=num+1#換人
            #print(len(QA))
            #print(QA)
            print("\n")
        #print(b)




if __name__ == '__main__':
    
    try:
        print(chromedriver_autoinstaller.get_chrome_version())
    except Exception as e:
        print(f"Chrome Driver版本檢查失敗：{str(e)}")
        exit()

    try:
        browser = webdriver.Chrome()
        browser.get("https://www.google.com/")
        browser.quit()
    except Exception as e:
        print(f"Chrome瀏覽器無法啟動：{str(e)}")

        try:
            chromedriver_autoinstaller.install()
            print("成功下載和安裝最新版本的Chrome Driver，請重新啟動程式。")
            exit()
        except Exception as e:
            print(f"Chrome Driver下載和安裝失敗：{str(e)}")

    config = configparser.ConfigParser()
    config.read('data/accounts.ini')
    Account = config['Default']['Account']
    Password = config['Default']['Password']
    Amount = config['Default']['Amount']
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {"profile.peeasf_manager_enabled": False, "credentials_enable_service": False})
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})


    driver=webdriver.Chrome(chrome_options=options)
    aa=FBcrawl(driver,Account,Password,Amount)
    aa.login()
    time.sleep(2)
    aa.mult_web()
 
    
    

    
