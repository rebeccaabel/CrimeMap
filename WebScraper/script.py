from bs4 import BeautifulSoup
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


URI = 'mongodb+srv://rebeccaabel:StGzyB9rUeSaVF9i@cluster0.tgvserh.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(URI, server_api=ServerApi('1'))
db = client["CrimeMap"]
collection = db["crime_data"]
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

            crime_document = {
            "Type of news": news_type,
            "Location": location,
            "Date": date
        }
            

collection.insert_one(crime_document)


print("Type of News:", news_type)
print("Location:", location)
print("Date:", date)


client.close()



