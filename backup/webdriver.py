from selenium import webdriver 
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

 
url = "https://www.google.com" 
options = webdriver.FirefoxOptions() 
options.add_argument("--headless")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
driver.get(url)
print(driver.page_source)
