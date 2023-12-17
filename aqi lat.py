from selenium import webdriver
from time import sleep
import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
import warnings
import os

from selenium.webdriver.common.keys import Keys

os.chdir(r'C:\Users\kshit\Desktop\data science\aqi data')
df_st = pd.read_csv('stations.csv')
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('user-data-dir=' + r'C:\Users\kshit\AppData\Local\Google\Chrome\User Data')

driver = webdriver.Chrome(
    executable_path=r'C:\Users\kshit\.wdm\drivers\chromedriver\win32\86.0.4240.22\chromedriver.exe',
    options=options)


# driver.get('https://www.google.com/webhp?hl=en&sa=X&ved=0ahUKEwjArr6SkIHzAhWe4XMBHXUrCVUQPAgI')
# driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('hello')

def fill_coordinates(row):
    try:
        try:
            driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').clear()
            driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys(
                row.StationName + " latitude" + Keys.RETURN)
            sleep(1)
            text = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div').text
        except:
            driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').clear()
            driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys(
                row.StationName.split('-')[0] + "latitude" + Keys.RETURN)
            sleep(1)
            text = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div').text

        row.Latitude, row.Longitude = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", text)
        print(row.StationName, row.Latitude, row.Longitude)
    except:
        # driver.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').clear_field()
        pass
    return row


df_st = df_st.apply(fill_coordinates, axis='columns')
df_st.to_csv('stations_updated')
