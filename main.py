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




def import_credentials(source_file:str, service_app:str):
    with open(source_file, "r") as json_file:
        credentials_list = json.load(json_file)
        username = credentials_list['gmail']['username']
        password = credentials_list['gmail']['app-password']
        return username, password

def import_match_list(source_file:str, service_app:str):
    with open(source_file, "r") as json_file:
            match_list = json.load(json_file)
            return match_list
    

def import_html_email(html_source_file:str):
    with open(html_source_file, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    return html_content


def custom_html(imported_html, match_list):
    
    events_html = []
    today = datetime.now().strftime("%A %d %B %Y")
    imported_html = imported_html.replace("\n", "")

    for match in match_list:
        match_date = match['date']  # Assurez-vous que cela est au format YYYY-MM-DD

        if match_date == today:
            team1 = match['team1']['name']
            team1_flag = match['team1']['flag-url']
            team2 = match['team2']['name']
            team2_flag = match['team2']['flag-url']
            date = match['date']
            hour = match['hour']
            channel = match['channel']
            game_details_url = match['game-details-url']

            match_html = f"""
                        <h2>{date}</h2>
                        <div class="matchs-list">
                            <div class="match-info">
                                <p class="match-hour">{hour}</p>
                                <p class="teams">{team1} - {team2}</p>
                                <p class="channel">📺 A voir sur {channel}</p>
                                <p class="cta-infos"><a href="{game_details_url}">Plus d'info*</a></p>
                                <p class="source-infos">* Source Foot Mercato</p>
                            </div>
                            <hr />
                        </div>
            """
            events_html.append(match_html)
    # html_content_with_events = imported_html.format("\n".join(events_html))
    html_content_with_events = imported_html.replace("{match_details}","\n".join(events_html))
    return html_content_with_events


def send_email(sender, subject, message_body, receiver_emails, attachment_source, username, password):

    # Paramètres du serveur SMTP Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    # smtp_port = 465

    # Informations Gmail
    smtp_username = username
    smtp_password = password

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
   

    #Configuration du message
    msg = MIMEMultipart()
    msg.attach(MIMEText(message_body, 'html'))
    # msg.attach(part) 
    msg['Subject'] = subject
    msg['From'] = sender
    # msg['To'] = ', '.join(receiver_emails)  # Convertit la liste en une chaîne séparée par des virgules
    msg['To'] = receiver_emails  # Convertit la liste en une chaîne séparée par des virgules
    
    # Connexion au serveur SMTP de Gmail et envoi de l'e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(username, receiver_emails, msg.as_string())
    print(f"\nMessage sent to {receiver_emails} ! ")

def main():

    #Récupération des paramètres d'authentification
    source_file = "credentials\\app_password.json"
    service_app = "gmail"
    username, password = import_credentials(source_file, service_app)
    source_file = "calendrier.json"
    html_source_file = ".\\email.html"
    imported_html = import_html_email(html_source_file)
    match_list = import_match_list(source_file, service_app)
    customized_html = custom_html(imported_html, match_list)

    #Récupération des détails du mail
    # sender = f"Jodré DM"
    sender = f"🌍 CAN 2024 - Actu ⚽"
    subject ="Programme de la journée !"
    # recipients ="C:\\Users\\djodr\\Documents\\document.pdf"    
    recipients =""
    receiver_emails = ['djodre88@hotmail.com']
    
    message_body = customized_html

    try:
        if receiver_emails:  # Vérifie si la liste n'est pas vide
            for receiver in receiver_emails:
                send_email(sender, subject, message_body, receiver, recipients, username, password)
        else:
            print("La liste des destinataires est vide.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    main()
