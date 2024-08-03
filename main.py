from bs4 import BeautifulSoup
import requests


leagues_list = {
    "ENG": ["English Premier League", "EPL", "PL", "Premier League"],
    "ESP": ["La Liga", "Liga", "Spanish Top Flight"],
    "FRA": ["Ligue 1", "French League"],
    "ITA": ["Serie A", "Italian League"],
    "GER": ["Bundesliga", "German League"]
}

league_name = input("Which league's goal and assist stats do you want to see? ")
for item in leagues_list:
    if league_name in leagues_list[item]:
        selected_league = item

# URL of the webpage you want to scrape
url = F'https://www.espn.com/soccer/stats/_/league/{selected_league}.1/season/2023'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

# Send a GET request to the webpage
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse the HTML content
    players = {}
    soup = BeautifulSoup(response.text, 'html.parser')

    list = soup.find_all('div', class_="Table__Scroller")

    # GOALS
    goals = gappearances = ""
    gcounter = namecounter = 0
    member = list[0].find_all('tbody', class_="Table__TBODY")
    row = member[0].find_all('tr', class_="Table__TR Table__TR--sm Table__even")
    for item in row:
        player_info = item.find_all('td', class_="Table__TD")
        player_score = item.find_all('td', class_="tar Table__TD")
        for info_item in player_info:
            span = info_item.find_all('span')
            for span_item in span:
                player_name_club = span_item.find_all('a', class_="AnchorLink")
                if player_name_club:
                    if namecounter % 2 == 0:
                        name = player_name_club[0].text
                    else:
                        club = player_name_club[0].text
                    namecounter += 1
        for score_item in player_score:
            goals_per_game = score_item.find_all('span', class_="tar")
            if goals_per_game:
                if gcounter % 2 == 0:
                    gappearances = goals_per_game[0].text
                else:
                    goals = goals_per_game[0].text
                gcounter += 1
        print(f"Name: {name} | Club: {club} | Goals: {goals} | Appearances: {gappearances}")

    print("---------------------------------------------------------")
    # ASSISTS
    assists = aappearances = ""
    acounter = 0
    member = list[1].find_all('tbody', class_="Table__TBODY")
    row = member[0].find_all('tr', class_="Table__TR Table__TR--sm Table__even")
    for item in row:
        player_info = item.find_all('td', class_="Table__TD")
        player_score = item.find_all('td', class_="tar Table__TD")
        for info_item in player_info:
            span = info_item.find_all('span')
            for span_item in span:
                player_name_club = span_item.find_all('a', class_="AnchorLink")
                if player_name_club:
                    if namecounter % 2 == 0:
                        name = player_name_club[0].text
                    else:
                        club = player_name_club[0].text
                    namecounter += 1
        for score_item in player_score:
            assists_per_game = score_item.find_all('span', class_="tar")
            if assists_per_game:
                if acounter % 2 == 0:
                    aappearances = assists_per_game[0].text
                else:
                    assists = assists_per_game[0].text
                acounter += 1
        print(f"Name: {name} | Club: {club} | Assists: {assists} | Appearances: {aappearances}")

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
