# Jedha_DL
Projet ETL : Kayak

## Structure des dossiers

Les sources sont organisés de la manière suivante :
 - *root* :
   - *README.md* : documentation générale du projet 
   - *Projet_Kayak_vF.ipynb* : Notebook d'exploration des données et de run des scripts de scraping, création de datalake et ETL (contient les consignes Jedha du projet)
 - *Scraping* :
   - *Booking.py* : script Python du scraping du site Booking.fr
 - *src* : contient les fichiers .json créés avec le notebook Projet_Kayak_vF.ipynb, est vide car ces fichiers sont dans le .gitignore

## Prérequis

- python 3.12.x
- avoir les comptes suivants :
   - API openweathermap : créer un compte gratuit sur leur site
   - AWS : 
     - créer un bucket S3
     - créer une database PostgreSQL
- un fichier python *keys.py* qui contient les mots de passe suivants :
   - WEATHER_KEY="YOUR_PWD_openweathermap_API"
   - AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
   - AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
   - PWD_DB="YOUR_PWD_DB_AWS"
