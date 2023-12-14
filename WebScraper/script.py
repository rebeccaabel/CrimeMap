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
            # ...

            for details_element in details_elements:
                updated_time_element = details_element.select_one('.c-event__updated span.text span:nth-child(2)')
                updated_time = updated_time_element.text.strip() if updated_time_element else None

                preamble = details_element.select_one('.c-event__preamble').text.strip()
                text = details_element.select_one('.c-event__text').text.strip()

                title_and_location_element = details_element.select_one('.c-heading--3 span.u-text-decoration--underline')
                title_and_location = title_and_location_element.text.strip() if title_and_location_element else None

# Extract date using string manipulation from the title
                date_start = title_and_location.find(" ") + 1
                date_end = title_and_location.find(",", date_start)
                date_part = title_and_location[date_start:date_end].strip() if date_start != -1 and date_end != -1 else None

# Combine the date with the day
                day_start = title_and_location.find(" ") - 2
                day = title_and_location[day_start:date_start].strip() if day_start != -1 else None

                full_date = f"{day} {date_part}" if day and date_part else None

# Remove the date and day from the title_and_location
                title_and_location = title_and_location.replace(day, "").replace(date_part, "").replace(", ", "", 1).strip()

    # Print the extracted information for each article
                print("Updated Time:", updated_time)
                print("Date:", full_date)
                print("Title:", title_and_location)
                print("Preamble:", preamble)
                print("Event Text:", text)
                print("\n")

    # Check for duplicates in the MongoDB collection based on the date
                existing_record = collection.find_one({"title_and_location": title_and_location, "date": full_date})

                if existing_record:
                    print(f"Duplicate found for title {title_and_location} and date {full_date}. Skipping insertion.")
                else:
        # Create a dictionary to insert into the MongoDB collection
                    crime_data = {
                        "updated_time": updated_time,
                        "date": full_date,
                        "title_and_location": title_and_location,
                        "preamble": preamble,
                        "text": text
                    }

        # Insert the data into the MongoDB collection
                    collection.insert_one(crime_data)



        except NoSuchElementException:
            print("No more news articles. Exiting loop.")
            break

finally:
    driver.quit()




