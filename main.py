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


class FBcrawl:

    def __init__(self, driver,account, password):
        self.driver=driver
        self.account = account
        self.password = password
        self.FB_url = "https://www.facebook.com/"
        self.xlsxPath ='test.xlsx'
        self.webaddress_url ="data/webaddress.txt"

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
    def write(self,address,worksheet):
        self.driver.get(address)
        wb = op.load_workbook(self.xlsxPath)
        time.sleep(3)
        sheet = wb[worksheet]
        
        while True:
            firstcheck=driver.execute_script("return document.body.scrollHeight;")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Seccheck=driver.execute_script("return document.body.scrollHeight;")
            if(firstcheck==Seccheck):
                break
            time.sleep(3)
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            memberaccout = driver.find_elements(By.CLASS_NAME,"xt0psk2")
            memberanswer = driver.find_elements(By.CLASS_NAME,'x1gslohp')
            num=1
            
            for i in range(len(memberaccout)):
                print(memberaccout[i].text+" "+memberanswer[i].text)
                
                if (memberaccout[i].text==memberaccout[i-1].text) :
                    menber='C'+str(num)
                    print(menber) 
                    sheet[menber].value=memberanswer[i].text
                else:
                    num=num+1
                    menber='A'+str(num)
                    print(menber)
                    sheet[menber].value=memberaccout[i].text
                    sheet['B'+str(num)].value=memberanswer[i].text
                    
        except:
            print("ERROR")

        print("Successful")
        wb.save('test.xlsx')




if __name__ == '__main__':
    configFilename = 'data/accounts.ini'
    if not os.path.isfile(configFilename):
        with open(configFilename, 'a') as f:
            f.writelines(["[Default]\n", "Account= your account\n", "Password= your password"])
            print('input your username and password in accounts.ini')
            exit()
    # get account info from ini config file
    config = configparser.ConfigParser()
    config.read(configFilename)
    Account = config['Default']['Account']
    Password = config['Default']['Password']
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {"profile.peeasf_manager_enabled": False, "credentials_enable_service": False})
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})


    driver=webdriver.Chrome(chrome_options=options)
    aa=FBcrawl(driver,Account,Password)
    aa.login()
    aa.mult_web()
    
    
    