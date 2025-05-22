# Smash Cube

Un jeu d'arcade multijoueur inspiré de Smash Bros, développé par Sami Hmida et Mathieu Lienard.

## 📋 Sommaire
- [Présentation du projet](#présentation-du-projet)
- [Technologies utilisées](#technologies-utilisées)
- [Rôles et organisation](#rôles-et-organisation)
- [Structure algorithmique](#structure-algorithmique)
- [Axes d'amélioration](#axes-damélioration)

## 🎮 Présentation du projet

Pistol Hand est un mini-jeu d'arcade accessible à tous les niveaux, offrant une expérience simple, amusante et rapide. Inspiré de Smash Bros, le jeu propose une physique cartoonesque agréable, de la musique et une interface intuitive.

### 🎯 Fonctionnalités principales

- **Contrôles manette** : Support des manettes Xbox et PlayStation
- **Interface intuitive** : Navigation entièrement à la manette
- **Menu complet** :
  - Lancement du jeu
  - Détection des manettes
  - Visualisation du leaderboard
  - Paramètres sonores

### 🎲 Gameplay

Chaque joueur incarne un slime mignon avec les contrôles suivants :
- **Joystick gauche** : Déplacement
- **Joystick droit** : Visée du pistolet
- **Bouton 1** : Saut (depuis le sol uniquement)
- **Bouton 2** : Dash (temps de récupération long)
- **Bouton 3** : Tir (temps de récupération court)

### 💪 Système de combat

- **3 vies** par joueur
- **Barre de vie** individuelle
- **Deux types de mort** :
  1. Impact violent contre un mur/obstacle
  2. Dégâts de pistolet (perte de vie progressive)

### 🏆 Système de score

- Points calculés selon :
  - Nombre de vies restantes
  - Nombre de joueurs affrontés
- Leaderboard persistant
- Option de réinitialisation des scores

## 🛠️ Technologies utilisées

- **Python** : Langage principal pour la logique de jeu
- **Pygame** : Gestion des collisions et affichage
- **SQLite** : Stockage persistant des données

## 👥 Rôles et organisation

### Sami Hmida
- Développement des menus
- Gestion des paramètres musique
- Intégration complète des manettes
- Gameplay

### Mathieu Lienard
- Menu leaderboard
- Base de données
- Gameplay

## 📁 Structure algorithmique

Organisation en 4 dossiers principaux :
- `engine/` : Logiques du jeu
- `entities/` : Entités (POO)
- `scene/` : Scènes et menus
- `database/` : Base de données SQLite
- `assets/` : Ressources graphiques et sonores

## 🔮 Axes d'amélioration

1. **Animations**
   - Menus
   - Personnages
   - Effets de tir

2. **Gameplay**
   - Nouveaux objets
   - Power-ups
   - Armes supplémentaires

3. **Maps**
   - Nouvelles arènes
   - Plateformes mobiles
   - Effets visuels

4. **Support**
   - Manettes Nintendo Switch
   - Optimisations
   - Améliorations visuelles
