import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import openpyxl as op



Faaa="https://www.facebook.com/"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {"profile.peeasf_manager_enabled": False, "credentials_enable_service": False})
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})

bcca = "C:/Users/user/Desktop/fb_web_crawler-main/chromedriver.exe"
driver=webdriver.Chrome(executable_path=bcca,chrome_options=options)
driver.maximize_window()
driver.get(Faaa)
wb = op.load_workbook('C:/Users/user/Desktop/fb_web_crawler-main/test.xlsx')

def login(file):
    
    f = open(file, 'r')
    account=f.readline()
    peeasf=f.readline()
    print(account[:-1])
    print(peeasf[:-1])
    f.close()
    leeasd(account[:-1],peeasf[:-1])
    time.sleep(3)

def leeasd(acc,peeasf):
    time.sleep(3)
    try:
        print("login")
        inputemail = driver.find_element(By.NAME,"email")
        inputemail.send_keys(acc)
        intputpass = driver.find_element(By.NAME,"pass")
        intputpass.send_keys(peeasf)
        button= driver.find_element(By.NAME,"login")
        button.click()
    except:
        print("login error")
    finally:
        print("login success")
    
        

def goto_memberpage(driver,member_address):
    driver.get(member_address)
    
def write(adress,worksheet):
    goto_memberpage(driver,adress)
    time.sleep(3)
    sheet = wb[worksheet]
    for i in range(8):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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



login("data\login.txt")
time.sleep(8)
f=open("data\webaddress.txt","r")
webaddress=f.readlines()
for i in range(len(webaddress)):
    
    print(webaddress[i][:-1])
    write(webaddress[i][:-1],'工作表'+str(i+1))
    time.sleep(8)


f.close()
driver.close()


