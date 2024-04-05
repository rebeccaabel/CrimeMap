from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from pymongo.server_api import ServerApi

load_dotenv()

url = "https://polisen.se/aktuellt/polisens-nyheter/"

mongo_uri = os.getenv("MONGO_URI")
db_name = "crime_dataDB"
collection_name = "crimes"

driver = webdriver.Chrome()
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client[db_name]
collection = db[collection_name]


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

try:
    driver.get(url)
    while True:
        try:
            print("Page loaded successfully!")

            # Extract information from the loaded page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            details_elements = soup.find_all('details', class_='c-expandable c-event')

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

                #extract the link
                link_element = details_element.select_one('.c-link')
                link = link_element['href'] if link_element else None

                article_data = {
                    "updated_time": updated_time,
                    "date": full_date,
                    "title": title_and_location,
                    "preamble": preamble,
                    "text": text,
                    "link": link
                }
                #collection.insert_one(article_data)

                # Print the extracted information for each article
                print("Updated Time:", updated_time)
                print("Date:", full_date)
                print("Title:", title_and_location)
                print("Preamble:", preamble)
                print("Event Text:", text)
                print("Link:", link)
                print("\n")

                next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='o-pagination__next']"))
                )

                next_button.click()

                time.sleep(3)

        except NoSuchElementException:
            print("No more news articles. Exiting loop.")
            break

finally:
    driver.quit()
    client.close()



