import urllib.parse as urlparse
from time import sleep

from fyers_api import fyersModel, accessToken
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

app_id = 'DQLFCI2ZKU-100'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('user-data-dir=' + r'C:\Users\kshit\AppData\Local\Google\Chrome\User Data')
session = accessToken.SessionModel(client_id="",
                                   secret_key="", redirect_uri="https://myapi.fyers.in/docs/",
                                   response_type="code", grant_type="authorization_code")

response = session.generate_authcode()
print(response)
url = session.generate_authcode()

driver = webdriver.Chrome(
            executable_path=r'C:\Users\kshit\.wdm\drivers\chromedriver\win32\86.0.4240.22\chromedriver.exe',
            options=options)
driver.get(url)
sleep(3)
current_url = driver.current_url
driver.get('https://trade.fyers.in/')

parsed = urlparse.urlparse(current_url)
auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
session.set_token(auth_code)
response = session.generate_token()
print(response['access_token'])
access_token = response['access_token']

fyers = fyersModel.FyersModel(client_id=app_id, token=access_token, log_path=r"C:\Users\kshit\PycharmProjects\Fyers_bot")
fyers.get_profile()

print(fyers.get_profile())
