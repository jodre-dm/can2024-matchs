# CAN 2024 - Programme Email

Ce projet Python envoie un email quotidien avec le programme des matchs pour la Coupe d'Afrique des Nations 2024 (CAN 2024).

## Description

Le programme récupère les informations des matchs depuis le site Foot Mercato, génère un email au format HTML avec les détails des matchs du jour, et envoie l'email à l'utilisateur.

## Fonctionnalités

- Scraping des informations des matchs depuis Foot Mercato.
- Génération d'un email HTML avec le programme des matchs du jour.
- Envoi automatique de l'email quotidien.

## Installation

1. Clonez le repository :

    ```bash
    git clone https://github.com/jodre-dm/can2024-matchs.git
    cd can2024-matchs
    ```

2. Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Créez un fichier `credentials/app_password.json` avec vos informations d'authentification Gmail :

    ```json
    {
        "gmail": {
            "username": "votre-adresse-email@gmail.com",
            "app-password": "votre-mot-de-passe-app"
        }
    }
    ```

2. Modifiez le fichier `calendrier.json` avec les matchs de la CAN 2024.

## Utilisation

Exécutez le script principal pour envoyer l'email quotidien :

```bash
python main.py


## Technologies

Python
SMTP (Simple Mail Transfer Protocol)
Web Scraping (Beautiful Soup)
HTML


## Contribution

Si vous souhaitez contribuer, veuillez soumettre une pull request avec vos modifications. Assurez-vous de suivre les règles de contribution.
