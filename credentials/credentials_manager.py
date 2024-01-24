import json


class CredentialsManager:
    def __init__(self, source_file):
        self.source_file = source_file
        self.import_credentials()

    def import_credentials(self):
        with open(self.source_file, "r", encoding='utf-8') as json_file:
            credentials_list = json.load(json_file)
            self.username = credentials_list['gmail']['username']
            self.password = credentials_list['gmail']['app-password']

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password

