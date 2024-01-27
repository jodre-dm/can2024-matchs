from src.match_list_handler import MatchListHandler
from src.html_generator import HTMLGenerator
from src.email_sender import EmailSender

from datetime import datetime

hour = datetime.now().strftime("%H:%M")

def main():
    #Import des matchs
    # match_list_source = "data/can-calendrier-poules.json"
    match_list_source = "data/can-2024-huitiemes-matchs.json"
    match_list_handler = MatchListHandler(match_list_source)
    match_list = match_list_handler.import_match_list()

    #Création du contenu du mail
    html_source_file = "templates/email_template.html"
    html_generator = HTMLGenerator(html_source_file)
    imported_html = html_generator.import_html_email()
    customized_html = html_generator.custom_html(imported_html, match_list)

    #Création du html généré
    html_generator.generate_html_file(customized_html)

    #Envoi de l'email
    credentials_source_file = "credentials/app_password.json"
    email_sender = EmailSender(credentials_source_file)

    #Paramétrage des créneaux d'envoi
    # dev_timeslots = ["00:01", "06:30", "15:56", "17:50", "18:40", "20:50"]
    dev_timeslots = ["01:17"]
    run_timeslots = ["09:00"]

    message_body = customized_html
    attachment_source = ""    
    
    
    #Choix des destinataires en fonction de l'heure
    if hour in dev_timeslots:
        sender = f"🌍 CAN 2024 🐘 🇨🇮 - Calendrier ⚽"
        subject ="MODE DEV - Mail checking"
        receivers = [{'name':'Jodré','email':'djodre88@hotmail.com'}]

    if hour in run_timeslots:
        sender = f"🌍 CAN 2024 🐘 🇨🇮 - Calendrier ⚽"
        subject ="Programme de la journée !"
        receivers = [
            {'name':'Jodré','email':'djodre88@hotmail.com'},
            {'name':'Abdoulaye','email':'ablos_1@hotmail.com'},
            {'name':'Jado','email':'jzoukra@gmail.com'},
            {'name':'Meriem','email':'haddache92@gmail.com'},
            {'name':'Vanneck','email':'sabyvanneck@gmail.com'},
            {'name':'Oumar','email':'oumardrame091@gmail.com'},
            {'name':'Précilia','email':'mavinga.liya@gmail.com'},
            {'name':'Vincent','email':'vincent.enyeka@gmail.com'},
            {'name':'Jean-Marc','email':'jean.marc.mukuta@gmail.com'},
            {'name':'Yves','email':'yves.mavindi@gmail.com'}
        ]


    try:
        if receivers:  # Vérifie si la liste n'est pas vide
            for receiver in receivers:
                email_sender.send_email(sender, subject, message_body, receiver, attachment_source)
        else:
            print("\nLa liste des destinataires est vide.")
    except Exception as e:
        # print(f"Une erreur s'est produite : {e}")
        print("\nLa liste des destinataires est vide.\n")


if __name__ == "__main__":
    main()
