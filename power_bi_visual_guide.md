# Guide de Création Visuelle du Rapport Power BI

Ce guide vous aidera à concevoir un rapport Power BI visuellement attrayant et informatif pour présenter la segmentation client Spotify.

## 1. Thème et Design Général
- **Couleurs** : Utilisez une palette de couleurs inspirée de Spotify (vert foncé, noir, gris, avec des accents de vert vif). Par exemple :
  - Arrière-plan : `#121212` (Noir Spotify)
  - Texte principal : `#FFFFFF` (Blanc)
  - Accents/Graphiques : `#1DB954` (Vert Spotify)
  - Texte secondaire/Légendes : `#B3B3B3` (Gris clair)
- **Polices** : Montserrat pour les titres et Open Sans pour le corps du texte, pour une cohérence avec la présentation.
- **Disposition** : Privilégiez une disposition claire et aérée, avec des espaces blancs suffisants entre les visuels.

## 2. Pages du Rapport et Visuels Suggérés

### Page 1 : Vue d'Ensemble de la Segmentation
Cette page servira de tableau de bord principal, offrant un aperçu rapide des segments clés.

- **Carte (Card) : Nombre Total d'Utilisateurs**
  - Affiche la mesure `Total Users`.
  - Position : En haut à gauche.
- **Carte (Card) : Nombre d'Utilisateurs Premium**
  - Affiche la mesure `Premium Users`.
  - Position : À côté de la carte précédente.
- **Graphique en Anneau (Donut Chart) : Répartition par Plan d'Abonnement**
  - Champ : `subscription_plan` (Légende), `Total Users` (Valeurs).
  - Mettez en évidence le pourcentage d'utilisateurs Premium.
  - Position : En haut à droite.
- **Graphique à Barres Empilées (Stacked Bar Chart) : Répartition des Utilisateurs par Tranche d'Âge**
  - Axe : `age_group`.
  - Valeurs : `Total Users`.
  - Position : Au centre de la page.
- **Graphique à Barres (Bar Chart) : Genres Préférés par Tranche d'Âge**
  - Axe : `age_group`.
  - Légende : `preferred_genre`.
  - Valeurs : `Total Users`.
  - Position : En bas de la page.

### Page 2 : Analyse Détaillée des Comportements
Cette page approfondira les comportements d'écoute et l'impact des Top 10 musiques.

- **Graphique à Barres (Bar Chart) : Fréquence d'Écoute par Plan d'Abonnement**
  - Axe : `listening_frequency`.
  - Légende : `subscription_plan`.
  - Valeurs : `Total Users`.
  - Position : En haut à gauche.
- **Graphique à Barres (Bar Chart) : Mood Dominant par Tranche d'Âge**
  - Axe : `age_group`.
  - Légende : `listening_mood`.
  - Valeurs : `Total Users`.
  - Position : En haut à droite.
- **Tableau : Top 10 Musiques et Leurs Écoutes**
  - Colonnes : `track_title`, `artist_name`, `genre`, `Listens by Top 10 Genre`.
  - Filtrez pour n'afficher que les `track_id` de 1 à 10.
  - Position : Au centre de la page.
- **Graphique à Barres (Bar Chart) : Appareils d'Écoute par Tranche d'Âge**
  - Axe : `age_group`.
  - Légende : `device_type`.
  - Valeurs : `Total Listens`.
  - Position : En bas de la page.

## 3. Interactivité et Filtres
- **Slicers (Segments)** : Ajoutez des slicers pour `age_group`, `gender`, `subscription_plan` sur les deux pages pour permettre une exploration dynamique des données.
- **Filtres de Page** : Utilisez les filtres de page pour affiner les données affichées (ex: filtrer les Top 10 musiques sur la Page 2).
- **Actions de Détail (Drill-through)** : Configurez des actions de détail pour passer d'un graphique récapitulatif à une vue plus granulaire si nécessaire (ex: cliquer sur une tranche d'âge pour voir les utilisateurs spécifiques).

## 4. Bonnes Pratiques
- **Titres Clairs** : Assurez-vous que chaque visuel et chaque page ont des titres clairs et concis.
- **Légendes** : Utilisez des légendes pour faciliter la compréhension des couleurs et des catégories.
- **Cohérence** : Maintenez une cohérence visuelle sur l'ensemble du rapport (couleurs, polices, taille des éléments).
- **Performance** : Évitez un nombre excessif de visuels sur une seule page pour garantir une bonne performance du rapport.

En suivant ce guide, vous pourrez créer un rapport Power BI percutant qui mettra en valeur les insights de votre segmentation client Spotify.
