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
2. **Visual Studio Code** :
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

---

## 📜 License


Distribuée sous la licence [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Voir le fichier LICENSE pour plus d'informations.



## 💡 Prochaines étapes
- **Créer une application mobile.**
- **Intégrer une API cartographique pour suivre les initiatives.**
- **Ajouter des badges pour récompenser les utilisateurs actifs.**

**Rejoignez l'aventure et changez le monde, une action à la fois ! 🌍**
```

