from bs4 import BeautifulSoup
import requests

url = "https://polisen.se/aktuellt/polisens-nyheter/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

details_tags = soup.find_all("details")

for details_tag in details_tags: 
    summary = details_tag.find("summary")
    news_type = summary.text if summary else "N/A"

    details_content = details_tag.find("div", class_="details-content")
    location_date = details_content.text if details_content else "N/A"

    print("Type of news:", news_type)
    print("Location and Date:", location_date)