import requests
from bs4 import BeautifulSoup

def get_league_code(league_name):
    leagues_list = {
        "ENG": ["English Premier League", "EPL", "PL", "Premier League"],
        "ESP": ["La Liga", "Liga", "Spanish Top Flight"],
        "FRA": ["Ligue 1", "French League"],
        "ITA": ["Serie A", "Italian League"],
        "GER": ["Bundesliga", "German League"]
    }
    for code, names in leagues_list.items():
        if league_name in names:
            return code
    return None

def scrape_league_stats(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None
    return response.text

def parse_stats(soup):
    players = {}
    stats = []
    list = soup.find_all('div', class_="Table__Scroller")

    for idx, stat_type in enumerate(["Goals", "Assists"]):
        member = list[idx].find_all('tbody', class_="Table__TBODY")
        row = member[0].find_all('tr', class_="Table__TR Table__TR--sm Table__even")
        for item in row:
            player_info = item.find_all('td', class_="Table__TD")
            player_score = item.find_all('td', class_="tar Table__TD")
            player = {"Name": "", "Club": "", stat_type: "", "Appearances": ""}
            namecounter = gcounter = 0
            for info_item in player_info:
                span = info_item.find_all('span')
                for span_item in span:
                    player_name_club = span_item.find_all('a', class_="AnchorLink")
                    if player_name_club:
                        if namecounter % 2 == 0:
                            player["Name"] = player_name_club[0].text
                        else:
                            player["Club"] = player_name_club[0].text
                        namecounter += 1
            for score_item in player_score:
                stat_value = score_item.find_all('span', class_="tar")
                if stat_value:
                    if gcounter % 2 == 0:
                        player["Appearances"] = stat_value[0].text
                    else:
                        player[stat_type] = stat_value[0].text
                    gcounter += 1
            stats.append(player)
    
    return stats

def print_stats(stats):
    for stat in stats:
        print(f"Name: {stat['Name']} | Club: {stat['Club']} | Goals: {stat.get('Goals', '')} | Assists: {stat.get('Assists', '')} | Appearances: {stat['Appearances']}")

def goals_and_assists(league_name):
    selected_league = get_league_code(league_name)
    if not selected_league:
        print(f"League '{league_name}' not found.")
        return
    
    url = f'https://www.espn.com/soccer/stats/_/league/{selected_league}.1/season/2023'
    page_content = scrape_league_stats(url)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        stats = parse_stats(soup)
        print_stats(stats)

# Example usage
if __name__ == "__main__":
    league_name = "English Premier League"
    goals_and_assists(league_name)
