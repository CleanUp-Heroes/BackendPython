[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)  
![Latest release](https://img.shields.io/github/v/release/cleanUp-Heroes/BackendPython)

[![Java CI Gradle build and test](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/build.yml)  [![SonarQube Cloud](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/sonar.yml/badge.svg)](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/sonar.yml)  [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=bugs)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)  [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)

---

## CleanUp Heroes
Adjedomole, Barry, Rahim

## Description de l'application
Ce site a pour ambition de sensibiliser les citoyens au tri sélectif et au respect de l’environnement tout en les encourageant à agir activement pour améliorer leur cadre de vie. Les utilisateurs peuvent participer à des **challenges environnementaux** qui leur permettent de gagner des points en réalisant des actions concrètes, telles que le tri des déchets ou la participation à des initiatives locales. Ces points accumulés pourront, à l’avenir, être échangés contre des récompenses concrètes, renforçant ainsi leur motivation à s’impliquer durablement.

En parallèle, le site offre une fonctionnalité clé : le **signalement de déchets abandonnés** dans les espaces publics. Ces signalements sont actuellement affichés sous forme de liste, mais une évolution future prévoit l’intégration d’une carte interactive. Chaque signalement sera représenté par un marqueur géolocalisé, offrant une vue claire des zones concernées. Une fois un déchet ramassé, son marqueur pourra être retiré de la carte pour refléter la propreté retrouvée de l’espace. Cette fonctionnalité vise à améliorer la coordination entre citoyens et services responsables, tout en fournissant un outil visuel pour mesurer les progrès réalisés.

Le site mettra également en avant des **classements mondiaux et locaux**, permettant aux utilisateurs de comparer leurs contributions avec celles des autres. Ces classements encourageront une saine compétition et renforceront le sentiment de communauté autour de la cause environnementale.

L’objectif global de ce projet est de promouvoir des comportements responsables, tels que le tri sélectif et la collecte des déchets, tout en récompensant l’engagement des utilisateurs. En combinant des éléments ludiques comme les challenges et les classements, des outils pratiques comme la carte interactive, et des perspectives d’avenir avec des récompenses concrètes, ce site ambitionne de devenir une plateforme incontournable pour tous ceux qui souhaitent agir pour l’environnement.

---
## CleanUp Heroes - Backend

## Instructions de démarrage

### 1. Prérequis

Assurez-vous d'avoir les outils suivants installés sur votre système :
- **Python** 3.8 ou version ultérieure
- **pip** (gestionnaire de paquets Python)
- **virtualenv** (optionnel, recommandé pour isoler l'environnement Python)
- **MySQL Workbench** (ou toute autre base de données compatible avec Django)
- **Asciidoctor** et **Asciidoctor-pdf** (pour générer la documentation)

---

### 2. Installation

1. **Clonez le dépôt :**
   ```bash
   git clone https://github.com/CleanUp-Heroes/BackendPython.git
   cd BackendPython
   ```

2. **Créez un environnement virtuel (recommandé) :**
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Démarrez le serveur de développement :**
   ```bash
   python manage.py runserver
   ```
   Accédez à l'application à l'adresse suivante : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 3. Configuration de la base de données MySQL

1. **Installez MySQL** : Assurez-vous que MySQL est installé et en cours d'exécution sur votre machine. Vous pouvez télécharger MySQL depuis [le site officiel](https://dev.mysql.com/downloads/).

2. **Créez une base de données** : Connectez-vous à votre serveur MySQL et créez une base de données pour l'application.
   ```sql
   CREATE DATABASE cleanup_heroes;
   ```

3. **Configurez les paramètres de la base de données dans Django** :
   Dans le fichier `settings.py` de votre projet Django, modifiez la section `DATABASES` pour y indiquer les informations de connexion à votre base de données MySQL :
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'cleanup_heroes',
           'USER': 'votre_utilisateur_mysql',
           'PASSWORD': 'votre_mot_de_passe_mysql',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

4. **Exécutez les migrations** : Une fois la configuration terminée, appliquez les migrations pour créer les tables nécessaires dans la base de données :
   ```bash
   python manage.py migrate
   ```

---

## Documentation

### 1. Swagger
La documentation API Swagger est automatiquement générée et accessible à l'adresse suivante :  
[http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)  

Swagger fournit un aperçu interactif des points d'API disponibles dans ce backend.

---

### 2. Asciidoctor

La documentation technique peut être générée en **HTML** et **PDF** grâce à Asciidoctor.  
Pour cela, vous devez d'abord installer Ruby et les gems nécessaires :

1. **Installer Ruby** : Téléchargez Ruby depuis [le site officiel](https://rubyinstaller.org/).
   
2. **Installer les gems nécessaires** : Une fois Ruby installé, ouvrez un terminal et exécutez la commande suivante :
   ```bash
   gem install asciidoctor asciidoctor-pdf
   ```

Ensuite, vous pouvez générer les fichiers de documentation :

1. **Génération du fichier HTML :**
   ```bash
   asciidoctor app/docs/asciidoc/main.adoc
   ```

2. **Génération du fichier PDF :**
   ```bash
   asciidoctor-pdf app/docs/asciidoc/main.adoc
   ```

Les fichiers générés se trouveront dans le répertoire `docs`.

---

## License

Ce projet est sous licence [Apache 2.0](LICENSE.txt).

---

## CleanUp Heroes - Frontend

### 🛠️ Technologies utilisées
- **Vue.js** : Framework JavaScript pour construire des interfaces utilisateur modernes.
- **Axios** : Gestion des appels HTTP et interaction avec l'API backend.
- **Node.js & npm** : Pour gérer les dépendances et exécuter les scripts.

### 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :
1. **Node.js** (version 16 ou supérieure recommandée) :
   - Téléchargez et installez depuis [nodejs.org](https://nodejs.org).
   - Vérifiez la version installée :
     ```bash
     node -v
     npm -v
     ```

2. Exécutez la commande suivante pour installer **Axios** via npm :
   ```bash
   npm install axios
   ```


3. **Visual Studio Code** :
   - Téléchargez et installez depuis [code.visualstudio.com](https://code.visualstudio.com/).

### 🧩 Extensions Visual Studio Code (si vous utilisez VSC)

Voici les extensions essentielles pour travailler sur ce projet. Vous pouvez les installer rapidement avec les commandes suivantes :

#### 1. **Vue Language Features (Volar)**
   ```bash
   ext install Vue.volar
   ```

#### 2. **ESLint**
   ```bash
   ext install dbaeumer.vscode-eslint
   ```
#### 3. **mapbox-gl**
   ```bash
 npm install mapbox-gl
   ```
Une fois l'installation terminée, vérifie que mapbox-gl est bien ajouté dans ton fichier package.json, sous "dependencies" :

```bash
"dependencies": {
  "mapbox-gl": "^x.x.x"
}
```
Après l'installation de mapbox-gl, redémarre le serveur de développement pour vérifier que l'erreur est résolue :

```bash
npm run serve
```

### 🚀 Démarrer le projet

1. Clonez le dépôt du frontend :
   ```bash
   git clone https://github.com/CleanUp-Heroes/Frontend.git
   cd Frontend
   ```

2. Installez les dépendances :
   ```bash
   npm install
   ```

3. Lancez l'application Vue.js :
   ```bash
   npm run serve
   ```
   Accédez à l'application à l'adresse suivante : [http://localhost:8080](http://localhost:8080)

### 📜 Structure des répertoires

- **src/axios** : Configuration des appels API.
- **src/assets** : Contient les ressources statiques (images, fichiers CSS, etc.).
- **src/components** : Composants Vue.js réutilisables dans l'application.
- **src/router** : Définition des routes pour la navigation dans l'application.
- **src/views** : Pages principales de l'application.

---

### tests unitaires
   cd Frontend
npm install --save-dev @vue/test-utils jest vue-jest @babel/preset-env babel-jest

## Auteurs

- [Claire ADJEDOMOLE](https://github.com/orgs/CleanUp-Heroes/people/ClaireAdjedomole)
- [Ibtissem RAHIM](https://github.com/orgs/CleanUp-Heroes/people/Ibtissem-01)
- [Mariam BARRY](https://github.com/orgs/CleanUp-Heroes/people/mariam896)
