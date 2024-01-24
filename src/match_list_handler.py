import json


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
