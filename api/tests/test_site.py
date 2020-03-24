from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")

browser = webdriver.Chrome(
    executable_path=r"C:\Users\Raihan\OneDrive\Hobi\Ongoing Projects\Raffle Web\API\Raven-Raffles\tests\chromedriver.exe",
    chrome_options=chrome_options)

browser.get('http://127.0.0.1:5000/')
browser.find_element_by_css_selector("#username_login").send_keys("a")
browser.find_element_by_css_selector("#pwd_login").send_keys("a")
browser.find_element_by_css_selector("button[type=submit]").click()

browser.get('http://127.0.0.1:5000/raffles/6')
browser.find_element_by_css_selector("button[type=submit]").click()

browser.get('http://127.0.0.1:5000/tasks')
browser.find_element_by_css_selector("#start-tasks").click()
