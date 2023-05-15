import requests
from bs4 import BeautifulSoup

# Make a request to the web page
url = 'https://www.last.fm/music/Mot%C3%B6rhead/Ace+of+Spades'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find an element by its tag name
# element = soup.find()

element = soup.find("div", {"id": "tracklist"})
# element = soup.find(id='chartlist')
# element.find("div", {"class": ""})

# Print the element's text content
print(element.txt)