from src.match_list_handler import MatchListHandler
from src.html_generator import HTMLGenerator
from src.email_sender import EmailSender

import json
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
today_date = datetime.now().strftime("%A %-d %B %Y")    
hour = datetime.now().strftime("%H:%M")

#Chargement du fichier de config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

admin_mode = config["admin-mode"]
run_mode = config["run-mode"]


def main():
    match_list_source = config["match_list_source"]
    match_list_handler = MatchListHandler(match_list_source)
    match_list = match_list_handler.import_match_list()

    #paramétrage du mail
    credentials_source_file = config["credentials_source_file"]
    email_sender = EmailSender(credentials_source_file)
    sender = f"🌍 CAN 2024 🐘 🇨🇮 - Calendrier ⚽"    
    attachment_source = config["attachment_source"]

    #Création du contenu du mail
    html_source_file = config["html_source_file"]
    html_generator = HTMLGenerator(html_source_file)
    imported_html = html_generator.import_html_email()
    customized_html = html_generator.custom_html(imported_html, match_list)
    simple_html = html_generator.simple_html(imported_html)

    #Paramétrage des créneaux d'envoi
    dev_timeslots = hour
    admin_timeslots = admin_mode["timeslots"]
    run_timeslots = run_mode["timeslots"]

    is_game_day = match_list_handler.game_day()  #booléen qui indique si nous sommes un jour de match

    if not is_game_day:
        message_body = simple_html
        html_generator.generate_html_file(simple_html) #Création du fichier html généré
        
    else:
        message_body = customized_html        
        html_generator.generate_html_file(customized_html) #Création du fichier html généré

        #Choix des destinataires en fonction de l'heure            
        if hour in admin_timeslots:
            subject ="MODE ADMIN - Mail checking"
            receivers = admin_mode["receivers"]

        if hour in run_timeslots:
            subject ="Programme de la journée !"
            receivers = run_mode["receivers"]

    if hour in dev_timeslots:
        subject ="MODE DEV - Mail checking"
        receivers = admin_mode["receivers"]
    
    #Envoi de l'email
    try:
        if receivers:  # Vérifie si la liste n'est pas vide
            for receiver in receivers:
                email_sender.send_email(sender, subject, message_body, receiver, attachment_source)
        else:
            print("\nLa liste des destinataires est vide.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        print("\nLa liste des destinataires est vide.\n")

if __name__ == "__main__":
    main()
