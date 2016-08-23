import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pypyodbc

dataset=[]
area =[]
connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost;'
                                'Database=tax;'
                                'uid=sa;'
                                'pwd=sa1')
cursor = connection.cursor()
SQLCommand = ("SELECT ID,[pickup_longitude],[pickup_latitude],[dropoff_longitude],[dropoff_latitude]FROM [tax].[dbo].[Yellow_New]")
cursor.execute(SQLCommand)
#results = cursor.fetchone()
for row in cursor.fetchall():
    dataset.append({'ID':row['ID'],'lon':row["pickup_longitude"],'lat':row["pickup_latitude"],'type':'p','paddress':''})
    dataset.append({'ID':row['ID'],'lon':row["dropoff_longitude"],'lat':row["dropoff_latitude"],'type':'d','daddress':''})
connection.close()
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, query):
    driver.get("http://maplarge.com/reversegeocoding")


    for d in dataset:
        box = driver.wait.until(EC.presence_of_element_located(
           (By.ID, "LatInput")))
        box.clear()

        box2 = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "LngInput")))
        box2.clear()
        box.send_keys(d["lon"])
        box2.send_keys(d["lat"])

        btton= driver.find_element_by_id('ReverseButton')
        btton.click()
        txt= driver.find_element_by_id('OutputDiv')
        print(txt.text)
        time.sleep(10)
        #if d["type"]=='p':
        #    dataset[d['ID']].paddress=txt.text
        #else:
        #    dataset[d['ID']].daddress=txt.text
if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "")
    time.sleep(50)
    driver.quit()