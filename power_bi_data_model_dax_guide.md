# Guide pour le Modèle de Données et les Mesures DAX dans Power BI

Ce guide vous aidera à configurer le modèle de données et à créer les mesures DAX essentielles pour votre rapport Power BI de segmentation client Spotify.

## 1. Importation des Données
Importez les trois fichiers CSV suivants dans Power BI Desktop :
- `spotify_users.csv`
- `spotify_tracks.csv`
- `spotify_listening_history.csv`

## 2. Modèle de Données (Relationships)
Créez les relations suivantes entre les tables :
- **`spotify_users`** et **`spotify_listening_history`** :
  - Type de relation : Many-to-One (`spotify_listening_history[user_id]` vers `spotify_users[user_id]`)
  - Cardinalité : Many to 1
  - Direction du filtre croisé : Single
- **`spotify_tracks`** et **`spotify_listening_history`** :
  - Type de relation : Many-to-One (`spotify_listening_history[track_id]` vers `spotify_tracks[track_id]`)
  - Cardinalité : Many to 1
  - Direction du filtre croisé : Single

## 3. Mesures DAX Essentielles
Voici quelques mesures DAX que vous pouvez créer pour l'analyse :

### a. Nombre Total d'Utilisateurs
```dax
Total Users = COUNTROWS(spotify_users)
```

### b. Nombre Total d'Écoutes
```dax
Total Listens = COUNTROWS(spotify_listening_history)
```

### c. Nombre d'Utilisateurs Premium
```dax
Premium Users = CALCULATE(
    COUNTROWS(spotify_users),
    spotify_users[subscription_plan] = "Premium"
)
```

### d. Pourcentage d'Utilisateurs Premium
```dax
% Premium Users = DIVIDE([Premium Users], [Total Users])
```

### e. Écoutes par Genre (pour les Top 10 Musiques)
Cette mesure peut être utilisée avec un visuel pour montrer les écoutes des genres des Top 10.
```dax
Listens by Top 10 Genre = 
CALCULATE(
    [Total Listens],
    KEEPFILTERS(spotify_tracks[track_id] IN {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
)
```

### f. Nombre d'Utilisateurs par Tranche d'Âge
Cette mesure est implicitement gérée par le glisser-déposer de `age_group` et `Total Users` dans un visuel, mais peut être explicitement définie si nécessaire.
```dax
Users by Age Group = CALCULATE(
    [Total Users],
    ALLEXCEPT(spotify_users, spotify_users[age_group])
)
```

## 4. Colonnes Calculées (Optionnel)

### a. Tranche d'Âge Catégorielle (si non déjà présente)
Si votre colonne d'âge est numérique, vous pouvez créer une colonne catégorielle :
```dax
Age Category = 
SWITCH(
    TRUE(),
    spotify_users[age] <= 20, "12-20",
    spotify_users[age] <= 35, "20-35",
    spotify_users[age] <= 60, "35-60",
    "60+"
)
```
*(Note : Dans notre CSV `spotify_users.csv`, la colonne `age_group` est déjà catégorielle, donc cette colonne calculée n'est pas strictement nécessaire mais est fournie à titre d'exemple.)*

## 5. Optimisation du Modèle
- **Masquer les colonnes clés** : Masquez les colonnes `user_id` et `track_id` dans les tables `spotify_users` et `spotify_tracks` une fois les relations établies. Elles ne sont pas nécessaires pour les visuels finaux et peuvent encombrer la vue.
- **Renommer les colonnes** : Renommez les colonnes pour les rendre plus lisibles dans le rapport (ex: `age_group` en "Tranche d'Âge").
