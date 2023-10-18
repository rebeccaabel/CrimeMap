from bs4 import BeautifulSoup
import requests
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from geopy.geocoders import Nominatim


URI = 'mongodb+srv://rebeccaabel:StGzyB9rUeSaVF9i@cluster0.tgvserh.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(URI, server_api=ServerApi('1'))
db = client["CrimeMap"]
collection = db["crime_data"]

collection.create_index("Date", unique=True)

geolocator = Nominatim(user_agent="crime_mapper") # Initialize

try: 
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


url = "https://polisen.se/aktuellt/polisens-nyheter/"  
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
details_tags = soup.find_all("details")

for details_tag in details_tags:

    summary = details_tag.find("summary")
    if summary:
        summary_text_element = summary.find("span", class_="u-text-decoration--underline")
        if summary_text_element:
            summary_text = summary_text_element.text

            parts = summary_text.split(",")
            if len(parts) == 3:
                date = parts[0].strip()
                news_type = parts[1].strip()
                location = parts[2].strip()
            else:
                date = "N/A"
                news_type = "N/A"
                location = "N/A"

            location_data = None
            retries = 3
            for i in range(retries):
                try:
                    location_data = geolocator.geocode(location)
                    if location_data:
                        lat = location_data.latitude
                        lon = location_data.longitude
                        break
                except Exception as e:
                    print(f"Geocoding attempt {i + 1} failed: {e}")
                    time.sleep(2) 

            if location_data is None:
                lat, lon = None, None

            crime_document = {
            "Type of news": news_type,
            "Location": location,
            "Date": date,
            "Latitude": lat,  
            "Longitude": lon 

            }
            try:
                collection.insert_one(crime_document)
            except DuplicateKeyError:
                pass

            print("Type of News:", news_type)
            print("Location:", location)
            print("Date:", date)
            print("Latitude:", lat)
            print("Longitude:", lon)


client.close()



