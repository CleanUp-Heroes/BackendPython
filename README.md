# BackendPython
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)  
![Latest release](https://img.shields.io/github/v/release/cleanUp-Heroes/BackendPython)

[![Java CI Gradle build and test](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/build.yml)  [![SonarQube Cloud](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/sonar.yml/badge.svg)](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/sonar.yml)  [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=bugs)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)

---

## Introduction

BackendPython est le backend du projet CleanUp Heroes, développé en Python avec Django.  
Il gère les fonctionnalités principales de l'application, y compris les défis, les participations des utilisateurs et les statistiques associées.

---

## Instructions de démarrage

### 1. Prérequis

Assurez-vous d'avoir les outils suivants installés sur votre système :
- **Python** 3.8 ou version ultérieure
- **pip** (gestionnaire de paquets Python)
- **virtualenv** (optionnel, recommandé pour isoler l'environnement Python)
- **MySQL Workbench** (ou toute autre base de données compatible avec Django)
- **Asciidoctor** (pour générer la documentation, facultatif)

---

### 2. Installation

1. **Clonez le dépôt :**
   ```bash
   git clone https://github.com/CleanUp-Heroes/BackendPython.git
   cd BackendPython
   ```

2. **Créez un environnement virtuel (recommandé) :**
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Démarrez le serveur de développement :**
   ```bash
   python manage.py runserver
   ```
   Accédez à l'application à l'adresse suivante : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Documentation

### 1. Swagger
La documentation API Swagger est automatiquement générée et accessible à l'adresse suivante :  
[http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)  

Swagger fournit un aperçu interactif des points d'API disponibles dans ce backend.

---

### 2. Asciidoctor

La documentation technique peut être générée en **HTML** et **PDF** grâce à Asciidoctor.  
Pour cela, exécutez les commandes suivantes :

1. **Génération du fichier HTML :**
   ```bash
   asciidoctor app/docs/asciidoc/main.adoc
   ```

2. **Génération du fichier PDF :**
   ```bash
   asciidoctor-pdf app/docs/asciidoc/main.adoc
   ```

Les fichiers générés se trouveront dans le répertoire `docs`.

---

## License

Ce projet est sous licence [Apache 2.0](LICENSE.txt).
```
