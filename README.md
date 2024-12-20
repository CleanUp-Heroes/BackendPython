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

Je suis désolé pour la confusion précédente. Voici tout le texte en **Markdown** comme tu l'as demandé, structuré correctement avec tous les éléments et le formatage Markdown adapté :

```markdown
# CleanUp-Heroes - Frontend

## Construit avec
Ce projet utilise les technologies suivantes :

- **Vue.js** (pour le frontend)
- **Axios** (pour les appels API)

---

## Étapes d'installation

### 1. Cloner le repository

Ouvrez un terminal et clonez le projet sur votre machine locale en utilisant la commande suivante :

```bash
git clone https://github.com/CleanUp-Heroes/FrontEnd-Vue.git
```

### 2. Naviguer dans le dossier du projet

Allez dans le dossier du projet cloné :

```bash
cd nom-du-projet
```

### 3. Installer les dépendances

Une fois dans le dossier du projet, vous devez installer les dépendances nécessaires pour exécuter le projet avec la commande suivante :

```bash
npm install
```

Cette commande installera **Vue.js** et **Axios**, ainsi que toutes les autres dépendances définies dans le fichier `package.json`.

### 4. Démarrer l'application

Après avoir installé les dépendances, vous pouvez démarrer l'application avec la commande suivante dans le terminal :

```bash
npm run serve
```

Cela lancera l'application en mode développement sur le port 8080. Vous pouvez accéder à l'application via [http://localhost:8080](http://localhost:8080).

---

## Fonctionnalités principales

### 1. Vue.js (Frontend)

**Vue.js** est utilisé pour gérer l'interface utilisateur du projet. C'est un framework JavaScript progressif qui permet de créer des interfaces utilisateur interactives.

- **Structure du projet** : Le projet est basé sur des composants Vue regroupés dans le dossier `src/components`.
- **Vue Router** est utilisé pour gérer la navigation entre les différentes pages de l'application.

### 2. Axios (Appels API)

**Axios** est utilisé pour interagir avec le backend en envoyant des requêtes HTTP. Toutes les requêtes API sont gérées dans des fichiers JavaScript dédiés, généralement sous `src/services/`.

#### Exemple d'appel API avec Axios :
Dans un fichier comme `src/services/api.js`, vous trouverez des appels API comme celui-ci :

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:3001/api/';

export const getSignalements = async () => {
  try {
    const response = await axios.get(`${API_URL}signalements`);
    return response.data;
  } catch (error) {
    console.error("Il y a une erreur lors de l'appel API", error);
  }
};
```

Cela permet de récupérer les signalements depuis le backend et de les afficher dans l'interface utilisateur.

---

## Résolution des problèmes

### Problème de port déjà utilisé

Si le port 8080 est déjà utilisé sur votre machine, vous pouvez changer le port d'écoute en exécutant la commande suivante :

```bash
npm run serve -- --port 8081
```

### Problème avec Axios

Si les appels API échouent, assurez-vous que le serveur backend est bien démarré et que l'URL de l'API dans le fichier `api.js` correspond à celle du serveur backend.

---

## Auteurs

- **Nom de l'auteur 1** - *Développeur principal* - [NomAuteur1](https://github.com/NomAuteur1)
- **Nom de l'auteur 2** - *Développeur* - [NomAuteur2](https://github.com/NomAuteur2)
- **Nom de l'auteur 3** - *Développeur* - [NomAuteur3](https://github.com/NomAuteur3)
```

Ce texte est **entièrement en Markdown** et prêt à être utilisé dans un fichier `README.md`. Si tu rencontres d'autres problèmes ou si tu as besoin de modifications, je suis là pour t'aider.
