import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from credentials.credentials_manager import CredentialsManager


class EmailSender:
    def __init__(self, credential_file):
        self.credential_manager = CredentialsManager(credential_file)
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

    def send_email(self, sender, subject, message_body, receiver, attachment_source):
        # Informations Gmail
        smtp_username = self.credential_manager.get_username()
        smtp_password = self.credential_manager.get_password()

        #Informations destinataire
        receiver_name = receiver['name']
        receiver_email = receiver['email']

        #personnalisation du message
        message_body = message_body.replace("{name}", receiver_name)

        #gestion des pièces jointes
        try:
            with open(attachment_source, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = attachment_source.split('/')[-1]
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
            )
        except Exception as e:
            print(f"\nAucune pièce jointe")
            # print(f"Une erreur s'est produite : {e}")
            pass

        # Configuration du message
        msg = MIMEMultipart()
        msg.attach(MIMEText(message_body, 'html'))
        if 'part' in locals():
            msg.attach(part)

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver_email
        
        # Connexion au serveur SMTP et envoi de l'e-mail
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, receiver_email, msg.as_string())
        print(f"\nMessage sent to {receiver_name} ! \n")

