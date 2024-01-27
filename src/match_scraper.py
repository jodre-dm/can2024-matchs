import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import json
import os


sites_sources = {}

TV_SPORTS_URL_BASE = "https://tv-sports.fr/foot/"

CAN = "coupe-d-afrique-des-nations_tv/match-direct"
LIGUE1 = "ligue-1_tv/match-direct"
PREMIER_LEAGUE = "premier-league_tv/match-direct"
CHAMPIONS_LEAGUE = "ligue-des-champions_tv/match-direct"

# Définir la locale en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

def get_site_content(competition, url_base):
    url = f"{url_base}{competition}"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
    response = requests.get(url, headers=headers)
    html = response.content
    site_content = BeautifulSoup(html, 'html.parser')
    return site_content

def get_matchs_list(site_content):
    matchs_list = []
    competition = site_content.h3
    all_matchs = competition.next_sibling
    for element in all_matchs.contents:
        if element.name == "h4":
            date = element.text
            if "Aujourd'hui" in date:
                date = datetime.now().strftime("%A %d %B %Y")
            match_dict = {}
        elif element.name == "div":
            match_elements = element.contents
            teams = match_elements[0].contents[1].next_sibling.contents[0].contents[0].split("/") 
            hour = match_elements[3].contents[0].contents[1].text.replace("h", ":")
            channel = match_elements[4].contents[0].attrs['alt']
            match_dict = {}
            match_dict['team1'] = {}
            match_dict['team1']['name'] = teams[0].strip()
            # match_dict['team1']['flag-url'] = ""
            match_dict['team2'] = {}                    
            match_dict['team2']['name'] = teams[1].strip()
            # match_dict['team2']['flag-url'] = ""
            match_dict['date'] = date
            match_dict['hour'] = hour
            match_dict['game-details-url'] = ""
            match_dict['iso-datetime'] = ""
            match_dict['channel'] = channel
            
            matchs_list.append(match_dict)

            print(f"\n{date} à {hour} : \n{teams[0]} - {teams[1]}\nsur {channel}")
        else:
            pass
    return matchs_list

def get_country_code_from_json(matchs_list):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'data', 'countries-codes.json')

    with open(json_path, 'r', encoding='utf-8') as file:
        countries_json = json.load(file)
    
    for match in matchs_list:
        country1 = match['team1']['name']
        match['team1']['country-code'] = countries_json[country1]
        country2 = match['team2']['name']
        match['team2']['country-code'] = countries_json[country2]

        print(f"\n{match}")


    return matchs_list

def set_flag_url(matchs_list):
    for match in matchs_list:
        team1_country_code = match['team1']['country-code']
        team1_flag_url = f"https://flagcdn.com/w80/{team1_country_code.lower()}.png"
        match['team1']['flag-url'] = team1_flag_url
        team2_country_code = match['team2']['country-code']
        team2_flag_url = f"https://flagcdn.com/w80/{team2_country_code.lower()}.png"
        match['team2']['flag-url'] = team2_flag_url


def export_matchs_list_to_json(matchs_list):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'data', 'can-2024-huitiemes-matchs.json')
    with open(json_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(matchs_list, indent=4))


def main():
    site_content = get_site_content(CAN, TV_SPORTS_URL_BASE)
    matchs_list = get_matchs_list(site_content)
    matchs_list = get_country_code_from_json(matchs_list)
    set_flag_url(matchs_list)
    export_matchs_list_to_json(matchs_list)
    input("press to finish")


if __name__ == "__main__":
    main()