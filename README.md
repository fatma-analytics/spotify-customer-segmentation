# Projet de Segmentation Client Spotify

## 🚀 Description du Projet
Ce projet a pour objectif de réaliser une segmentation client approfondie pour Spotify, en se basant sur les comportements d'écoute et les données démographiques des utilisateurs, notamment en lien avec les Top 10 musiques. L'analyse permet d'identifier des profils d'utilisateurs distincts et de formuler des recommandations stratégiques pour optimiser les campagnes marketing et l'expérience utilisateur.

## 🎯 Objectifs
- Analyser les profils démographiques (tranches d'âge, genre) des utilisateurs Spotify.
- Segmenter l'audience en fonction des préférences musicales, des moods d'écoute et des plans d'abonnement.
- Évaluer l'impact des Top 10 musiques sur l'engagement des différents segments.
- Développer un script SQL pour la gestion et l'analyse des données.
- Créer une présentation des résultats pour les parties prenantes.
- Simuler un rapport Power BI interactif pour une exploration visuelle des données.

## 📂 Structure du Projet
```
spotify_segmentation_project/
├── spotify_segmentation_script.sql      # Script SQL de création de tables, insertion de données et requêtes de segmentation
├── spotify_segmentation_research.md     # Notes de recherche et synthèse des données Kaggle et Top 10 musiques
├── spotify_users.csv                    # Données synthétiques des utilisateurs (démographie, comportement)
├── spotify_tracks.csv                   # Données synthétiques des musiques (Top 10)
├── spotify_listening_history.csv        # Données synthétiques de l'historique d'écoute
├── power_bi_data_model_dax_guide.md     # Guide pour le modèle de données et les mesures DAX dans Power BI
├── power_bi_visual_guide.md             # Guide pour la conception visuelle du rapport Power BI
├── spotify_dashboard.py                 # Script Python pour générer le tableau de bord interactif (Plotly)
├── spotify_dashboard.html               # Tableau de bord interactif HTML généré par le script Python
├── spotify_presentation/                # Dossier contenant les fichiers HTML de la présentation
│   ├── cover.html
│   ├── objectives.html
│   ├── methodology.html
│   ├── demographics.html
│   ├── behavior_table.html
│   ├── premium_analysis.html
│   ├── top10_impact.html
│   ├── mood_context.html
│   ├── devices_access.html
│   ├── recommendations.html
│   └── conclusion.html
├── LICENSE                              # Fichier de licence MIT
└── README.md                            # Ce fichier
```

## 🛠️ Technologies Utilisées
- **SQL** : Pour la modélisation des données, l'insertion et les requêtes de segmentation.
- **Python (Pandas, Plotly)** : Pour l'analyse de données, la génération de données synthétiques et la création du tableau de bord interactif.
- **HTML/CSS/JavaScript (Chart.js, D3.js)** : Pour la création de la présentation interactive.
- **Power BI (conceptuel)** : Guides pour la modélisation et la visualisation des données.
- **GitHub** : Pour le contrôle de version et le partage du projet.

## ⚙️ Installation et Utilisation

### 1. Base de Données SQL
Pour recréer la base de données et exécuter les requêtes de segmentation :
1. Importez le fichier `spotify_segmentation_script.sql` dans votre système de gestion de base de données (MySQL, PostgreSQL, etc.).
2. Exécutez le script pour créer les tables, insérer les données synthétiques et visualiser les résultats des requêtes de segmentation.

### 2. Tableau de Bord Interactif (Python/Plotly)
Pour générer et visualiser le tableau de bord interactif :
1. Assurez-vous d'avoir Python 3.x installé, ainsi que les bibliothèques `pandas` et `plotly` (`pip install pandas plotly`).
2. Placez les fichiers `spotify_users.csv`, `spotify_tracks.csv`, `spotify_listening_history.csv` et `spotify_dashboard.py` dans le même répertoire.
3. Exécutez le script Python :
   ```bash
   python spotify_dashboard.py
   ```
4. Un fichier `spotify_dashboard.html` sera généré. Ouvrez-le dans votre navigateur web pour interagir avec le tableau de bord.

### 3. Présentation des Résultats
La présentation est disponible sous forme de fichiers HTML dans le dossier `spotify_presentation/`. Ouvrez `spotify_presentation/cover.html` dans votre navigateur pour commencer la présentation.

### 4. Guides Power BI
Les fichiers `power_bi_data_model_dax_guide.md` et `power_bi_visual_guide.md` fournissent des instructions détaillées pour recréer un rapport Power BI similaire en utilisant les fichiers CSV fournis.

## 📊 Résultats Clés
- Identification de quatre segments d'utilisateurs principaux (Gen Z, Millennials, Adultes, Seniors) avec des comportements d'écoute et des préférences musicales distincts.
- Les Millennials (20-35 ans) sont le segment le plus important pour les abonnements Premium et l'écoute quotidienne.
- Le Top 10 des musiques influence fortement l'engagement, avec des artistes comme Justin Bieber et Bruno Mars dominant certains segments.
- Des recommandations stratégiques ciblées ont été formulées pour la personnalisation, la rétention, l'acquisition et la diversification du contenu.

## 🎤 Présentation des Résultats
Accédez à la présentation interactive ici : [Lien vers la présentation](manus-slides://IoMJxp4MOYNnQITn0aIBSB)

## 📈 Rapport Power BI (Simulation)
Explorez le tableau de bord interactif simulant un rapport Power BI ici : [Lien vers le tableau de bord](https://8000-iwagyq2nexfndou72o0kj-34a9d3fe.us1.manus.computer/spotify_dashboard.html)

## ✍️ Auteur
Manus AI

## 📄 Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
