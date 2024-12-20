# BackendPython
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE.txt)
![Latest release](https://img.shields.io/github/v/release/cleanUp-Heroes/BackendPython)


[![Java CI Gradle build and test](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/build.yml)

[![SonarQube Cloud](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/sonar.yml/badge.svg)](https://github.com/CleanUp-Heroes/BackendPython/actions/workflows/sonar.yml)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=bugs)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=CleanUp-Heroes_BackendPython&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=CleanUp-Heroes_BackendPython)



# CleanUp-Heroes - Frontend



## Construit avec
Ce projet utilise les technologies suivantes :

- **Vue.js** (pour le frontend)
- **Axios** (pour les appels API)

---

## Étapes d'installation

### 1. Cloner le repository

Ouvrez un terminal et clonez le projet sur votre machine locale en utilisant la commande suivante :

git clone https://github.com/CleanUp-Heroes/FrontEnd-Vue.git

### 2. Naviguer dans le dossier du projet

Allez dans le dossier du projet cloné :

cd nom-du-projet

```markdown
# Fungikey

**Fungikey, l'application pour tout savoir sur les champignons.**



### Contexte
- De nombreuses applications similaires existent sur le marché, telles que :
  - **Champignouf**
  - **Aux champignons**
  - **Picture Mushroom**  
Ces applications, bien que populaires, sont axées sur la cueillette et l'identification par image, contrairement à **Fungikey 2024**, qui s'adresse à un public éducatif, notamment des étudiants en pharmacie.

---

## Construit avec
Les principaux frameworks et bibliothèques utilisés sont :
- **Node**
- **React**
- **Bootstrap**
- **JQuery**

---

## Manuel d'installation et d'utilisation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/Assem92/Fungikey
   ```
2. **Installer NodeJS :** Téléchargez et installez NodeJS.

3. **Lancer le backend :**
   - Accédez au répertoire `branches/fungikey-backend`.
   - Exécutez les commandes suivantes :
     ```bash
     npm install
     npm start
     ```
   - Le backend est disponible sur : [http://localhost:3001/](http://localhost:3001/).

4. **Lancer le frontend :**
   - Accédez au répertoire `branches/fungikey`.
   - Exécutez les commandes suivantes :
     ```bash
     npm install
     npm start
     ```
   - Le frontend est disponible sur : [http://localhost:3000/](http://localhost:3000/).

---

## Conteneurisation

1. **Installer Docker** : Téléchargez Docker [ici](https://www.docker.com/).
2. **Construire les images Docker :**
   ```bash
   docker build -t fungikey-backend -f fungikey-backend/Dockerfile fungikey-backend
   docker build -t fungikey-frontend -f Fungikey/Dockerfile Fungikey
   ```
3. **Lancer les conteneurs :**
   ```bash
   docker run -p 3000:3000 fungikey-frontend
   docker run -p 3001:3001 fungikey-backend
   ```
4. **Accéder à l'application :**
   - Frontend : [http://localhost:3000/](http://localhost:3000/)
   - Backend : [http://localhost:3001/](http://localhost:3001/)

5. **Arrêter les conteneurs :**
   ```bash
   docker stop [nom ou ID du conteneur]
   ```

---

## API

La documentation de l'API est accessible via Swagger : [http://localhost:3001/api-docs/](http://localhost:3001/api-docs/).

### Routes disponibles
- **Champignons :**
  - `GET /api/champi/` : Liste des champignons.
  - `GET /api/champi/{id}` : Champignon par ID.
  - `GET /api/familleChampi/` : Liste des familles de champignons.
  - `GET /api/familleComplementaires/` : Liste des familles complémentaires.

- **Recettes :**
  - `GET /api/recette/` : Liste des recettes.
  - `GET /api/recette/{id}` : Recette par ID.

- **Localisation :**
  - `GET /closest-points/:latitude/:longitude` : Retourne les 3 champignons les plus proches.
  - `POST /location` : Ajoute une nouvelle localisation de champignons.

- **Forum :**
  - `GET /posts` : Liste des publications.
  - `POST /posts` : Ajoute une nouvelle publication.

- **Produits :**
  - `POST /products` : Ajoute un nouveau produit.
  - `PUT /products/:id` : Met à jour un produit.
  - `DELETE /products/:id` : Supprime un produit.

- **Périodes :**
  - `GET /periodes` : Liste des périodes.
  - `GET /periodes/:id` : Détails d'une période.

---

## Contributions

Les contributions sont les bienvenues !  
Pour contribuer :
1. **Forker le projet.**
2. **Créer une branche pour vos modifications :**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Valider vos modifications :**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Pousser votre branche :**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Ouvrir une Pull Request.**

---




### 3. Installer les dépendances

Une fois dans le dossier du projet, vous devez installer les dépendances nécessaires pour exécuter le projet avec la commande suivante :

npm install

Cette commande installera **Vue.js** et **Axios**, ainsi que toutes les autres dépendances définies dans le fichier `package.json`.

### 4. Démarrer l'application

Après avoir installé les dépendances, vous pouvez démarrer l'application avec la commande suivante dans le terminal :


npm run serve


Cela lancera l'application en mode développement sur le port 8080. Vous pouvez accéder à l'application via [http://localhost:8080](http://localhost:8080).



## Fonctionnalités principales

### 1. Vue.js (Frontend)

**Vue.js** est utilisé pour gérer l'interface utilisateur du projet. C'est un framework JavaScript progressif qui permet de créer des interfaces utilisateur interactives.

- **Structure du projet** : Le projet est basé sur des composants Vue regroupés dans le dossier `src/components`.
- **Vue Router** est utilisé pour gérer la navigation entre les différentes pages de l'application.

### 2. Axios (Appels API)

**Axios** est utilisé pour interagir avec le backend en envoyant des requêtes HTTP. Toutes les requêtes API sont gérées dans des fichiers JavaScript dédiés, généralement sous `src/services/`.

Cela permet de récupérer les signalements depuis le backend et de les afficher dans l'interface utilisateur.

## License

Distribuée sous la licence **Apache 2.0**. Voir le fichier `LICENSE` pour plus d'informations.

## Auteurs

- **Nom de l'auteur 1** - *Développeur principal* - [NomAuteur1](https://github.com/NomAuteur1)
- **Nom de l'auteur 2** - *Développeur* - [NomAuteur2](https://github.com/NomAuteur2)
- **Nom de l'auteur 3** - *Développeur* - [NomAuteur3](https://github.com/NomAuteur3)
```
