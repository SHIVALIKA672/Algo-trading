import re
import sqlite3
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse as urlparse
from time import sleep
import datetime

conn = sqlite3.connect('stocks.db')
cur = conn.cursor()

cur.execute('SELECT cash FROM networth order by id DESC LIMIT 1;')
money = cur.fetchone()[0]
companies = {}


def action_to_take(company, details):
    global money
    details[0] = float(details[0])
    total_holdings = 0
    quantity = 0
    cur.execute("SELECT price,quantity from holdings where name = ?", (company,))
    rows = cur.fetchall()
    for row in rows:
        total_holdings += row[0] * row[1]
        quantity += row[1]
    if quantity != 0:
        avg = total_holdings / quantity
        # print(avg, total_holdings, quantity)
        if details[0] > avg:
            profit = details[0] * quantity - avg * quantity - 0.0003 * details[0] * quantity
            # print(company, profit)
            if profit > 80:
                print(company, profit)
                conn.execute('INSERT into transactions(name,price,quantity,date,type)  values(?,?,?,?,?)',
                             (company, details[0], quantity, datetime.datetime.now(), 'sold'))
                conn.execute('delete from holdings where name = ?', (company,))
                print("sold ", quantity, " shares of {} worth".format(company), quantity * details[0])
    else:
        if money > quantity * details[0]:
            quantity = int(8000 / details[0])
            if quantity != 0:
                conn.execute('INSERT into holdings(name,price,quantity,date)  values(?,?,?,?)',
                             (company, details[0], quantity, datetime.datetime.now()))
                conn.execute('INSERT into transactions(name,price,quantity,date,type)  values(?,?,?,?,?)',
                             (company, details[0], quantity, datetime.datetime.now(), 'bought'))
                money -= quantity * details[0]
                print("bought ", quantity, " shares of {} worth".format(company), quantity * details[0])


def fill_company(table):
    soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
    for sou in soup.find_all('div', attrs={'class': re.compile('^symbol.*')}):
        data = sou.find_all('span', attrs={'class': re.compile('^inner.*')})
        if len(data) < 2: continue
        conn.execute('INSERT or replace INTO company(NAME,price,change,change_percentage,volume) values(?,?,?,?,?)',
                     list(d.text for d in data))
    conn.commit()


def fetch_table_data(table):
    soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
    for sou in soup.find_all('div', attrs={'class': re.compile('^symbol.*')}):
        data = sou.find_all('span', attrs={'class': re.compile('^inner.*')})
        if len(data) < 2: continue
        companies[data[0].text] = list(data[n + 1].text for n in range(len(data) - 1))


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('user-data-dir=' + r'C:\Users\kshit\AppData\Local\Google\Chrome\User Data')

driver = webdriver.Chrome(
    executable_path=r'C:\Users\kshit\.wdm\drivers\chromedriver\win32\86.0.4240.22\chromedriver.exe',
    options=options)
driver.get('https://trade.fyers.in/')
sleep(5)
wait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath("/html/body/div[1]/iframe")))
table = driver.find_element_by_xpath(
    '/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div')
fetch_table_data(table)
fill_company(table)


def update_networth():
    pass
    cur.execute('insert or replace into networth ')


while True:
    conn.commit()
    fetch_table_data(table)
    for x, v in companies.items():
        action_to_take(x, v)
    # update_networth()
    sleep(0.5)
