from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import sys

latitude = ''  # Latitude of the specific area
longitude = ''  # Longitude of the specific area
query = 'hospital near me'

# Construct the URL with latitude, longitude, and search query
url = f"https://www.google.com/maps/@{latitude},{longitude},15z"

service = Service('C:\Windows\chromedriver.exe')  # Replace 'path/to/chromedriver' with the actual path
options = Options()
options.headless = True  # Run Chrome in headless mode
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)


# Perform your scraping operations here
search_box = driver.find_element(By.ID, 'searchboxinput')

search_box.send_keys(query)
search_box.send_keys(Keys.ENTER)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'qBF1Pd')))

scroll_pause_time = 2
last_results = None

while True:
    results = driver.find_elements(By.CLASS_NAME, 'qBF1Pd')
    if results == last_results:
        break

    last_results = results
    last_element = results[-1]
    driver.execute_script("arguments[0].scrollIntoView();", last_element)
    time.sleep(scroll_pause_time)

results = driver.find_elements(By.CLASS_NAME, 'qBF1Pd')
for r in results:
    try:
        print(r.text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
    except Exception as e:
        print(f"Error occurred: {str(e)}")

driver.quit()
