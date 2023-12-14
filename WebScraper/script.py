from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

# Load environment variables from .env
load_dotenv()

# Access environment variables
mongodb_uri = os.getenv("MONGODB_URI")

# MongoDB connection
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
db = client["CrimeMap"]
collection = db["crime_data"]

# Set up the webdriver with a fake user agent
user_agent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

# URL of the page you want to scrape
url = "https://polisen.se/aktuellt/polisens-nyheter/"
driver.get(url)

try:
    while True:
        try:
            # Wait for the "Visa fler" button to be present in the DOM
            xpath_expression = "//button[@class='police-element js-listpage-loadmore']"
            view_more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_expression))
            )

            print("Clicking the 'Visa fler' button...")
            # Use JavaScript to click the "Visa fler" button
            driver.execute_script("arguments[0].click();", view_more_button)

            # Introduce a delay between requests
            time.sleep(5)  # Adjust the sleep duration as needed

            print("Page loaded successfully!")

            # Extract information from the loaded page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Example: Extracting details, title, and event text for each article
            details_elements = soup.find_all('details', class_='c-expandable c-event')
            for details_element in details_elements:
                summary_text = details_element.find('summary', class_='c-expandable__summary').text.strip()
                title = details_element.find('h3', class_='c-heading--3').text.strip()
                event_text = details_element.find('div', class_='c-event__text').text.strip()

                # Print the extracted information for each article
                print("Summary:", summary_text)
                print("Title:", title)
                print("Event Text:", event_text)
                print("\n")

        except NoSuchElementException:
            print("No more news articles. Exiting loop.")
            break

except Exception as e:
    print("An error occurred: {e}")

finally:
    # Close the webdriver
    driver.quit()




