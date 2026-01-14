📱 ESN Mobile App – React Native

Application mobile destinée à une Entreprise de Services du Numérique (ESN) permettant de gérer les processus internes :
CRA / Timesheet, missions, staffing, RH et validations managers.

🎯 Objectifs du projet

Simplifier la saisie des temps (CRA)

Donner de la visibilité aux consultants et managers

Centraliser les processus RH

Réduire les erreurs de facturation

Améliorer l’expérience collaborateur

🧩 Fonctionnalités principales
✅ MVP (Minimum Viable Product)

Authentification (JWT / SSO)

Gestion des missions

Saisie des temps (jour / semaine)

Historique des CRA

Validation manager

Notifications

🔜 Fonctionnalités futures

Mode offline

Export PDF

Signature électronique

Staffing & disponibilité

RH mobile (congés, documents)

Portail client

🛠️ Stack technique
Frontend

React Native

Expo

TypeScript

React Navigation

Zustand ou Redux Toolkit

React Hook Form

Axios

Day.js

Backend (non inclus dans ce repo)

API REST ou GraphQL

Node.js / NestJS

PostgreSQL

Auth JWT / OAuth2

📁 Architecture du projet
src/
 ├── api/            # Appels API
 ├── components/     # Composants UI réutilisables
 ├── features/       # Domaines métier
 │    ├── auth/
 │    ├── timesheet/
 │    ├── staffing/
 │    └── rh/
 ├── navigation/     # Navigation
 ├── store/          # State management
 ├── hooks/          # Hooks personnalisés
 ├── utils/          # Helpers
 └── theme/          # Styles & thèmes


Architecture orientée features pour faciliter la maintenance et la scalabilité.

🚀 Installation & lancement
Prérequis

Node.js >= 18

npm ou yarn

Expo CLI

Android Studio ou Xcode (optionnel)

Installation
git clone https://github.com/your-org/esn-mobile-app.git
cd esn-mobile-app
npm install

Lancement
npx expo start

🔐 Authentification & rôles

Rôles supportés :

Consultant

Manager

Admin

Gestion des accès basée sur les rôles côté frontend et backend.

📡 Communication API

Toutes les données sont récupérées via une API REST

Gestion des erreurs globales

Intercepteurs Axios pour le token JWT

📲 Notifications

Notifications push pour :

Validation CRA

Rappel saisie

Fin de mission

Congés validés

🧪 Qualité & bonnes pratiques

Code typé (TypeScript)

Séparation logique UI / métier

Composants réutilisables

Gestion centralisée des erreurs

Formatage avec ESLint & Prettier

📌 Roadmap

 Setup projet

 Authentification

 CRA / Timesheet

 Validation manager

 Mode offline

 RH mobile

 Staffing

 Portail client

👥 Équipe

Mobile : React Native

Backend : Node.js

Produit : ESN / Manager

UX/UI : optionnel

📄 Licence

Projet interne ESN – usage privé.

📬 Contact

Pour toute question ou évolution :
Responsable projet / Tech Lead
