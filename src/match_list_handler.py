import json
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
today_date = datetime.now().strftime("%A %-d %B %Y")  


class MatchListHandler:
    def __init__(self, source_file):
        self.source_file = source_file
        self.match_list = [] 

    def import_match_list(self):
        with open(self.source_file, "r", encoding='utf-8') as json_file:
            self.match_list = json.load(json_file)
            return self.match_list
        
    def get_match_list(self):
        return self.match_list
    
    def game_day(self):
        return self.match_list[0]['date'] == today_date
