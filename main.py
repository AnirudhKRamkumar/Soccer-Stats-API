from bs4 import BeautifulSoup
import requests

# name = input("What type of stats are you looking for?")

# URL of the webpage you want to scrape
url = f''

# Send a GET request to the webpage
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    players = {}
    soup = BeautifulSoup(response.text, 'html.parser')
