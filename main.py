# from . import match_scraper

# CAN = "afrique/coupe-dafrique-des-nations"
# LIGUE1 = "france/ligue-1"
# CHAMPIONS_LEAGUE = "europe/ligue-des-champions-uefa"
# URL_BASE = f"https://www.footmercato.net/programme-tv/"

# site_content = match_scraper.get_site_content(CAN)
# match_list = match_scraper.get_match_list()

import json
import smtplib
import hashlib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime

import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
today = datetime.now().strftime("%A %d %B %Y")


def import_credentials(source_file:str, service_app:str):
    with open(source_file, "r", encoding='utf-8') as json_file:
        credentials_list = json.load(json_file)
        username = credentials_list['gmail']['username']
        password = credentials_list['gmail']['app-password']
        return username, password


def import_match_list(source_file:str, service_app:str):
    with open(source_file, "r", encoding='utf-8') as json_file:
            match_list = json.load(json_file)
            return match_list
    

def import_html_email(html_source_file:str):
    with open(html_source_file, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    return html_content


def custom_html(imported_html, match_list, today_date=today):
    
    events_html = []
    
    imported_html = imported_html.replace("\n", "")

    for match in match_list:
        match_date = match['date']  # Assurez-vous que cela est au format YYYY-MM-DD

        if match_date == today_date:
            team1 = match['team1']['name']
            team1_flag = match['team1']['flag-url']
            team2 = match['team2']['name']
            team2_flag = match['team2']['flag-url']
            date = match['date'].upper()
            hour = match['hour']
            channel = match['channel']
            game_details_url = match['game-details-url']
            font_family = "font-family : system-ui,-apple-system,'Segoe U',Roboto,'Helvetica Neue',Arial,'Noto Sans','Liberation Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji';"
            cta_font_style = "font-size: .9em; color: white;"
            cta_color_style = "background: #064534; border-radius: 50px; padding: .7em .2em; width: 100px;margin: 20px auto; "
            team_flag_style = "max-width: 1.5em; margin-right: 3px;"
            line_height = "line-height: .6em"

            match_html = f"""
                        <br />
                        <h3 style="font-size: 1em;">{date}</h3>
                        <div class="matchs-list" style="{line_height}">
                            <div class="match-info">
                                <h3 class="match-hour" style="text-decoration: underline; font-size: 1em;{font_family}">{hour}</h3>
                                <p class="teams; {font_family}">
                                    <img src="{team1_flag}" data-src="{team1_flag}" alt="{team1}" class="matchTeam__logo" style="{team_flag_style}"> {team1} - \
                                    <img src="{team2_flag}" data-src="{team2_flag}" alt="{team2}" class="matchTeam__logo" style="{team_flag_style}"> {team2}</p>
                                <p class="channel; {font_family}">📺 A voir sur {channel}</p>
                                <p class="cta-infos;" style="{cta_color_style}"><a href="{game_details_url}" style="{font_family}{cta_font_style}">Plus d'info*</a></p>
                                <p class="source-infos;" style="{font_family}font-style:italic; font-size:.8em">* Source Foot Mercato</p>
                                <br />
                            </div>
                            <hr />
                        </div>
                        """           
            
            
            events_html.append(match_html)
    # html_content_with_events = imported_html.format("\n".join(events_html))
    html_content_with_events = imported_html.replace("{match_details}","\n".join(events_html))
    return html_content_with_events


def generate_html_file(customized_html):
    with open(f"generated_html_email_{today}.html", "w", encoding="utf-8") as html_file:
        html_file.write(customized_html)
        print("Fichier HTML enregistré avec succès.")
        return html_file


def send_email(sender, subject, message_body, receiver, attachment_source, username, password):

    # Paramètres du serveur SMTP Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    # smtp_port = 465

    # Informations Gmail
    smtp_username = username
    smtp_password = password

    receiver_name = receiver['name']
    receiver_email = receiver['email']


    message_body = message_body.replace("{name}", receiver_name)

    try:
        with open(attachment_source, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = attachment_source.split('\\')[-1]
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
        )
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        # print(f"Une erreur s'est produite : {e}")
        pass
   

    #Configuration du message
    msg = MIMEMultipart()
    msg.attach(MIMEText(message_body, 'html'))
    # msg.attach(part) 
    msg['Subject'] = subject
    msg['From'] = sender
    # msg['To'] = ', '.join(receiver_emails)  # Convertit la liste en une chaîne séparée par des virgules
    msg['To'] = receiver_email  # Convertit la liste en une chaîne séparée par des virgules
    
    # Connexion au serveur SMTP de Gmail et envoi de l'e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(username, receiver_email, msg.as_string())
    print(f"\nMessage sent to {receiver_name} ! \n")

def main():

    #Récupération des paramètres d'authentification
    source_file = "credentials\\app_password.json"
    service_app = "gmail"
    username, password = import_credentials(source_file, service_app)
    source_file = "calendrier.json"
    html_source_file = ".\\email.html"
    # html_source_file = ".\\email-test.html"
    imported_html = import_html_email(html_source_file)
    match_list = import_match_list(source_file, service_app)
    customized_html = custom_html(imported_html, match_list)
    html_file = generate_html_file(customized_html)

    #Récupération des détails du mail
    sender = f"🌍 CAN 2024 🐘 🇨🇮 - Calendrier ⚽"
    subject ="Programme de la journée !"
    # receivers = [{'name':'Jodré','email':'djodre88@hotmail.com'}]   
    
    # sender = f"TEST TABLE"
    # subject ="TEST"
    # receivers = [{'name':'Jodré','email':'djodre88@hotmail.com'}]

    recipients =""

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
    
    message_body = customized_html

    try:
        if receivers:  # Vérifie si la liste n'est pas vide
            for receiver in receivers:
                send_email(sender, subject, message_body, receiver, recipients, username, password)
        else:
            print("La liste des destinataires est vide.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    main()
