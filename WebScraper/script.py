from bs4 import BeautifulSoup
import requests

url = "https://polisen.se/aktuellt/polisens-nyheter/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

details_tags = soup.find_all("details")

# Loop through the details tags and extract the information from the summary text
for details_tag in details_tags:
    # Extract the summary text
    summary = details_tag.find("summary")
    if summary:
        summary_text_element = summary.find("span", class_="u-text-decoration--underline")
        if summary_text_element:
            summary_text = summary_text_element.text
            # Split the summary text to extract location and date
            parts = summary_text.split(",")
            if len(parts) == 3:
                date = parts[0].strip()
                news_type = parts[1].strip()
                location = parts[2].strip()
            else:
                date = "N/A"
                news_type = "N/A"
                location = "N/A"

            # Print the information
            print("Type of News:", news_type)
            print("Location:", location)
            print("Date:", date)
