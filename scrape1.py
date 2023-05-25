from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service

latitude = "51.5074"  # Latitude of the specific area
longitude = "-0.1278"  # Longitude of the specific area
query = input('Enter your query: ')

# Construct the URL with latitude, longitude, and search query
url = f"https://www.google.com/maps/@{latitude},{longitude},15z?q={query}"

service = Service('C:\Windows\chromedriver.exe')  # Replace 'path/to/chromedriver' with the actual path
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

# Perform your scraping operations here
search_box = driver.find_element(By.ID, 'searchboxinput')

search_box.send_keys(query)
search_box.send_keys(Keys.ENTER)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'qBF1Pd')))

results = driver.find_elements(By.CLASS_NAME, 'qBF1Pd')
for r in results:
    try:
        print(r.text)
    except StaleElementReferenceException:
        print("Stale element encountered. Skipping...")

driver.quit()
