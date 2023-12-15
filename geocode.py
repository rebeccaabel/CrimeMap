import re
from geopy.geocoders import Nominatim

# Sample MongoDB document
document = {
    "_id": {"$oid": "657b08d85a865694b0750ced"},
    "updated_time": "14 december 14.46",
    "date": "14 december 12.49",
    "title_and_location": "Brand, Oxelösund",
    "preamble": "Barnvagnbrand i trappuppgång",
    "text": "12:24 Polis och räddningstjänst larmades till Esplanaden i Oxelösunds centrum. En barnvagn hade av oklar anledning börjat brinna på nedre botten i en trappuppgång. Rök spred sig och boende fick in rök.\nBranden är släckt och ambulanspersonal kontroller om personer som andats in rök mår bra.\nPolisen utreder vad som inträffat.\n13:02 Polisen misstänker att branden var anlagd och öppnar därför en förundersökning rörande mordbrand.\nFem personer blev milt rökskadade varav ett barn. Platsen spärras av.\n14:10 Sju personer fördes till sjukhus för kontroll av rökskador.\n14:45 Totalt åtta personer fördes med ambulans till sjukhus för vård mot rökskador."
}

# Initialize geocoder
geolocator = Nominatim(user_agent="my_geocoder")

# Extract locations from different fields
location_fields = ["title_and_location", "preamble", "text"]
locations = []

for field in location_fields:
    matches = re.findall(r'\b(?:[A-ZÖÄÅa-zöäå.-]+(?:\s[A-ZÖÄÅa-zöäå.-]+)*)\b', document[field])
    for match in matches:
        location = geolocator.geocode(match)
        if location:
            locations.append({"name": match, "coordinates": (location.latitude, location.longitude)})

# Define a hierarchy of location types
location_hierarchy = ["area", "street", "city", "county"]

# Sort locations based on hierarchy
locations.sort(key=lambda loc: next((h for h in location_hierarchy if h in loc["name"].lower()), "country"))

# Determine the most specific location (last one in the sorted list)
most_specific_location = locations[-1] if locations else None

print("All locations found:", locations)
print("Most specific location:", most_specific_location)
