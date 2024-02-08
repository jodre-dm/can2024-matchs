import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import json
import os


FM_BASE_URL = f"https://www.footmercato.net/programme-tv/"

CAN = "afrique/coupe-dafrique-des-nations"
LIGUE1 = "france/ligue-1"
CHAMPIONS_LEAGUE = "europe/ligue-des-champions-uefa"


# Définir la locale en français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

def get_site_content(competition):
    url = f"{FM_BASE_URL}{competition}"
    response = requests.get(url)
    html = response.content
    site_content = BeautifulSoup(html, 'html.parser')
    return site_content

def get_match_list(site_content):
    games = site_content.find_all('div', attrs={'matchBroadcast'})
    i=0
    match_list = []
    for game in games:
        # if i<3:
        #     pass
        # else:
            game_details_endpoint = game.find('a', attrs={'matchBroadcast__link'}).get('href')
            game_details_url = f"https://www.footmercato.net{game_details_endpoint}"
            teams = game.find_all("span", attrs={'matchBroadcast__teams'})
            team1_name = teams[0].contents[1].text.strip('\n')
            team1_flag_url = teams[0].contents[1].contents[1].contents[1].attrs['data-src']
            teams[0].contents[1].contents[1].contents[1]
            team2_name = teams[0].contents[3].text.strip('\n')
            team2_flag_url = teams[0].contents[3].contents[1].contents[1].attrs['data-src']
            iso_datetime = game.contents[1].contents[1].contents[0].contents[1].attrs['datetime']
            original_date = datetime.fromisoformat(iso_datetime)
            # Ajouter une heure
            new_date = original_date + timedelta(hours=1)
            # Convertir la nouvelle date en string
            new_date_string = new_date.isoformat().replace('+00:00', '+01:00')
            # Convertir en objet datetime
            date_obj = datetime.fromisoformat(new_date_string)
            formatted_date = date_obj.strftime('%A %d %B %Y, %H:%M')
            channel = game.contents[3].contents[1].text

            match_dict = {}
            match_dict['team1'] = {}
            match_dict['team1']['name'] = team1_name
            match_dict['team1']['flag-url'] = team1_flag_url
            match_dict['team2'] = {}
            match_dict['team2']['name'] = team2_name
            match_dict['team2']['flag-url'] = team2_flag_url
            match_dict['date'] = date_obj.strftime('%A %d %B %Y')
            match_dict['hour'] = date_obj.strftime('%H:%M')
            match_dict['game-details-url'] = game_details_url
            match_dict['iso-datetime'] = new_date_string
            match_dict['channel'] = channel[9:]

            match_list.append(match_dict)

        # i+=1
    return match_list

def export_matchs_list_to_json(matchs_list, stage):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'data', f"can-2024-{stage}-matchs.json")
    with open(json_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(matchs_list, indent=4))

def main():
    stage = "dernier-carré"
    site_content = get_site_content(CAN)
    matchs_list = get_match_list(site_content)
    export_matchs_list_to_json(matchs_list, stage)
    print(matchs_list)


if __name__ == "__main__":
     main()