import requests
from bs4 import BeautifulSoup
import locale
import re
import pycountry
import os
import json


class Team:
    def __init__(self, name, position, team_type, country_code=None):
        self.name = name
        self.position = position
        self.team_type = team_type
        self.country_code = country_code if country_code else self._get_country_code()
        self.flag_url = self._set_flag_url()

    @classmethod
    def get_country_code_from_json(cls, country_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '..', 'data', 'countries-codes.json')

        with open(json_path, 'r', encoding='utf-8') as file:
            countries_json = json.load(file)

        return countries_json.get(country_name, None)

    def _get_country_code(self):
        # Essayer de récupérer le code du pays à partir du JSON
        country_code = self.get_country_code_from_json(self.name)

        # Si le code du pays n'est pas trouvé dans le JSON, utilisez la recherche fuzzy
        if not country_code:
            try:
                country = pycountry.countries.search_fuzzy(self.name)
                if country:
                    country_code = country[0].alpha_2
            except AttributeError:
                pass

        return country_code
        

    def _set_flag_url(self):
        if self.team_type.lower() == "pays" and self.country_code:
            return f"https://flagcdn.com/w80/{self.country_code.lower()}.png"
        elif self.team_type.lower() == "club":
            # URL par défaut pour les clubs, si nécessaire
            return "url_du_drapeau_du_club"
        else:
            return "url_par_defaut"

    def __str__(self):
        return f"{self.name} ({self.team_type}, {self.position}) - Flag: {self.flag_url}"

class Match:
    def __init__(self, date, teams, hour, channel):
        self.date = date
        self.teams = teams
        self.hour = hour
        self.channel = channel

    def display(self):
        print(f"\n{self.date} à {self.hour} :\n{self.teams[0]} - {self.teams[1]}\nsur {self.channel}")

class MatchScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_site_content(self, competition):
        url = f"{self.base_url}{competition}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = response.content
            site_content = BeautifulSoup(html, 'html.parser')
            return site_content
        else:
            print(f"Erreur lors de la récupération du contenu. Code de statut : {response.status_code}")
            return None

    def get_matches(self, competition):
        site_content = self.get_site_content(competition)
        if site_content:
            matchs_dates = site_content.find_all("h4")
            matches = []
            for date in matchs_dates:
                if re.search(r"Aujourd'hui|\b2024\b", date.text):
                    match_elements = date.next_sibling.next_sibling.contents
                    teams = match_elements[0].contents[1].next_sibling.contents[0].contents[0].split("/")
                    hour = match_elements[3].contents[0].contents[1].text.replace("h", ":")
                    channel = match_elements[4].contents[0].attrs['alt']

                    team1 = Team(name=teams[0].strip(), position="Domicile", team_type="Pays")
                    team2 = Team(name=teams[1].strip(), position="Extérieur", team_type="Pays")

                    # Utilisation de la méthode _get_country_code pour récupérer les codes de pays
                    team1.country_code = team1._get_country_code()
                    team2.country_code = team2._get_country_code()

                    matches.append(Match(date=date.text, teams=[team1, team2], hour=hour, channel=channel))
            return matches
        else:
            return []

def main():
    TV_SPORTS_URL_BASE = "https://tv-sports.fr/foot/"
    CAN = "coupe-d-afrique-des-nations_tv/match-direct"

    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    scraper = MatchScraper(TV_SPORTS_URL_BASE)
    matches = scraper.get_matches(CAN)

    for match in matches:
        match.display()


if __name__ == "__main__":
    main()