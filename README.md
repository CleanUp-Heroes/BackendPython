# BackendPython
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

## Objectif de l'application
L’objectif global de ce projet est de promouvoir des comportements responsables, tels que le tri sélectif et la collecte des déchets, tout en récompensant l’engagement des utilisateurs. En combinant des éléments ludiques comme les challenges et les classements, des outils pratiques comme la carte interactive, et des perspectives d’avenir avec des récompenses concrètes, ce site ambitionne de devenir une plateforme incontournable pour tous ceux qui souhaitent agir pour l’environnement.

---

## Instructions de démarrage

### 1. Prérequis

Assurez-vous d'avoir les outils suivants installés sur votre système :
- **Python** 3.8 ou version ultérieure
- **pip** (gestionnaire de paquets Python)
- **virtualenv** (optionnel, recommandé pour isoler l'environnement Python)
- **MySQL Workbench** (ou toute autre base de données compatible avec Django)
- **Asciidoctor** et **Asciidoctor-pdf** (pour générer la documentation)

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
Pour cela, vous devez d'abord installer Ruby et les gems nécessaires :

1. **Installer Ruby** : Téléchargez Ruby depuis [le site officiel](https://rubyinstaller.org/).
   
2. **Installer les gems nécessaires** : Une fois Ruby installé, ouvrez un terminal et exécutez la commande suivante :
   ```bash
   gem install asciidoctor asciidoctor-pdf
   ```

Ensuite, vous pouvez générer les fichiers de documentation :

1. **Génération du fichier HTML :**
   ```bash
   asciidoc -b html5 app/docs/asciidoc/main.adoc
   ```

2. **Génération du fichier PDF :**
   ```bash
   asciidoc -b pdf app/docs/asciidoc/main.adoc
   ```

Les fichiers générés se trouveront dans le répertoire `docs`.

---

## License

Ce projet est sous licence [Apache 2.0](LICENSE.txt).






# Cleanup Heroes - Frontend

✨ **Un projet qui connecte les héros de l'environnement à des actions concrètes pour un monde plus propre !** ✨



## 🛠️ Technologies utilisées
- **Vue.js** : Framework JavaScript pour construire des interfaces utilisateur modernes.
- **Axios** : Gestion des appels HTTP et interaction avec l'API backend.
- **Node.js & npm** : Pour gérer les dépendances et exécuter les scripts.



## 📋 Prérequis

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

3. **Visual Studio Code** :
   - Téléchargez et installez depuis [code.visualstudio.com](https://code.visualstudio.com/).


## 🧩 Extensions Visual Studio Code ( si vous utilisez VSC)

Voici les extensions essentielles pour travailler sur ce projet. Vous pouvez les installer rapidement avec les commandes suivantes :

### 1. **Vue Language Features (Volar)**
   ```bash
   ext install Vue.volar
   ```

### 2. **ESLint**
   ```bash
   ext install dbaeumer.vscode-eslint
   ```

### 3. **Prettier - Code Formatter**
   ```bash
   ext install esbenp.prettier-vscode
   ```

### 4. **Vetur (Optionnel)**
   ```bash
   ext install octref.vetur
   ```

Pour exécuter ces commandes, ouvrez **Visual Studio Code**, appuyez sur `Ctrl+P` (ou `Cmd+P` sur Mac), entrez `>` suivi de la commande ci-dessus.

---

## 🖥️ Installation et exécution du projet

### Étape 1 : Cloner le dépôt
```bash
git clone https://github.com/CleanUp-Heroes/FrontEnd-Vue.git
cd FrontEnd-Vue
```

### Étape 2 : Installer les dépendances
```bash
npm install
```

### Étape 3 : Lancer le serveur de développement
```bash
npm run serve
```

### Étape 4 : Accéder à l'application
- **Local** : [http://localhost:8080](http://localhost:8080)
- **Réseau** : Suivez l'URL indiquée dans le terminal, par exemple [http://172.16.73.48:8080](http://172.16.73.48:8080).

---

## 🛠️ Résolution des problèmes fréquents

### 1. **Erreur : Module introuvable**
   - Supprimez et réinstallez les dépendances :
     ```bash
     rm -rf node_modules
     npm install
     ```

### 2. **Le serveur ne démarre pas**
   - Assurez-vous que le port 8080 est disponible ou modifiez-le dans le fichier `vue.config.js`.

### 3. **Problème de formatage**
   - Configurez Prettier comme formatteur par défaut dans VS Code :
     - Allez dans les **Paramètres** (`Ctrl+,` ou `Cmd+,`).
     - Recherchez `Format on Save` et cochez la case.

---

## 🌍 Contribuer

✨ **Devenez un héros du code et aidez Cleanup Heroes à grandir !** ✨

### Pourquoi contribuer ?
Votre code ne fera pas que fonctionner : il aura un impact écologique direct ! Que vous corrigiez un bug, ajoutiez une nouvelle fonctionnalité, ou amélioriez la documentation, chaque contribution compte.

### Comment contribuer ?
1. **Forker le dépôt** :
   - Cliquez sur le bouton `Fork` en haut à droite du dépôt GitHub.

2. **Cloner votre fork** :
   ```bash
   git clone https://github.com/votre-utilisateur/FrontEnd-Vue.git
   cd FrontEnd-Vue
   ```

3. **Créer une branche pour votre contribution** :
   ```bash
   git checkout -b feature/nom-de-la-fonctionnalité
   ```

4. **Apporter vos modifications** :
   - Suivez les bonnes pratiques de développement et exécutez `npm run lint` avant de valider.

5. **Valider vos modifications** :
   ```bash
   git add .
   git commit -m "Ajout : [Description de votre modification]"
   ```

6. **Envoyer vos modifications** :
   ```bash
   git push origin feature/nom-de-la-fonctionnalité
   ```

7. **Ouvrir une Pull Request (PR)** :
   - Rendez-vous sur votre fork et cliquez sur `New Pull Request`.

---

## 🏆 Remerciements

Nous remercions toutes les personnes qui ont contribué à rendre ce projet possible :
- Les développeurs passionnés.
- Les utilisateurs qui nous aident à nous améliorer.
- La communauté des héros environnementaux.


## 📜 License


Distribuée sous la licence [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Voir le fichier LICENSE pour plus d'informations.



## 💡 Prochaines étapes
- **Créer une application mobile.**
- **Intégrer une API cartographique pour suivre les initiatives.**
- **Ajouter des badges pour récompenser les utilisateurs actifs.**

**Rejoignez l'aventure et changez le monde, une action à la fois ! 🌍**
