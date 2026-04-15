-- Script SQL pour la segmentation client Spotify

-- 1. Création des tables

-- Table des Utilisateurs (Démographie et Comportement)
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    age_group VARCHAR(20) NOT NULL, -- '12-20', '20-35', '35-60', '60+'
    gender VARCHAR(20) NOT NULL,
    usage_period VARCHAR(50) NOT NULL, -- '< 6 months', '6 months - 1 year', '1-2 years', '> 2 years'
    subscription_plan VARCHAR(20) NOT NULL, -- 'Free', 'Premium'
    preferred_genre VARCHAR(50) NOT NULL,
    listening_mood VARCHAR(50) NOT NULL,
    listening_frequency VARCHAR(50) NOT NULL
);

-- Table des Musiques (Top 10 et autres)
CREATE TABLE tracks (
    track_id INT PRIMARY KEY AUTO_INCREMENT,
    artist_name VARCHAR(100) NOT NULL,
    track_title VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    release_year INT
);

-- Table des Interactions (Historique d'écoute)
CREATE TABLE listening_history (
    interaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    track_id INT NOT NULL,
    listen_date DATETIME NOT NULL,
    device_type VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);

-- 2. Insertion de données synthétiques

-- Données pour la table 'users'
INSERT INTO users (age_group, gender, usage_period, subscription_plan, preferred_genre, listening_mood, listening_frequency) VALUES
('20-35', 'Female', '1-2 years', 'Premium', 'Pop', 'Energetic', 'Daily'),
('12-20', 'Male', '< 6 months', 'Free', 'Hip Hop', 'Relaxed', 'Several times a week'),
('35-60', 'Male', '> 2 years', 'Premium', 'Rock', 'Focused', 'Daily'),
('20-35', 'Female', '6 months - 1 year', 'Free', 'R&B', 'Sad', 'Occasionally'),
('60+', 'Female', '> 2 years', 'Premium', 'Jazz', 'Relaxed', 'Daily'),
('12-20', 'Male', '< 6 months', 'Free', 'Pop', 'Energetic', 'Several times a week'),
('20-35', 'Female', '1-2 years', 'Premium', 'Electronic', 'Party', 'Daily'),
('35-60', 'Male', '> 2 years', 'Free', 'Classical', 'Relaxed', 'Occasionally'),
('20-35', 'Female', '6 months - 1 year', 'Premium', 'Hip Hop', 'Energetic', 'Daily'),
('12-20', 'Male', '< 6 months', 'Free', 'Pop', 'Happy', 'Several times a week');

-- Données pour la table 'tracks' (basées sur les Top 10)
INSERT INTO tracks (artist_name, track_title, genre, release_year) VALUES
('Justin Bieber', 'Beauty And A Beat', 'Pop', 2012),
('SWIM', 'Babydoll', 'Indie Pop', 2023),
('Bruno Mars', 'Risk It All', 'R&B', 2024),
('PinkPantheress', 'Stateside', 'Electronic', 2023),
('Justin Bieber', 'Confident', 'Pop', 2013),
('Djo', 'End of Beginning', 'Psychedelic Pop', 2022),
('Dave', 'Raindance', 'Hip Hop', 2023),
('Tems', 'Man I Need', 'Afrobeats', 2024),
('Tame Impala', 'Dracula (Remix)', 'Psychedelic Rock', 2023),
('Olivia Dean', 'So Easy', 'Soul', 2022);

-- Données pour la table 'listening_history'
INSERT INTO listening_history (user_id, track_id, listen_date, device_type) VALUES
(1, 1, '2024-03-10 10:00:00', 'Mobile'),
(2, 2, '2024-03-10 11:00:00', 'Desktop'),
(3, 3, '2024-03-10 12:00:00', 'Smart Speaker'),
(4, 1, '2024-03-10 13:00:00', 'Mobile'),
(5, 4, '2024-03-10 14:00:00', 'Desktop'),
(1, 5, '2024-03-11 09:00:00', 'Mobile'),
(2, 6, '2024-03-11 10:00:00', 'Desktop'),
(3, 7, '2024-03-11 11:00:00', 'Smart Speaker'),
(4, 8, '2024-03-11 12:00:00', 'Mobile'),
(5, 9, '2024-03-11 13:00:00', 'Desktop'),
(1, 10, '2024-03-12 08:00:00', 'Mobile'),
(2, 1, '2024-03-12 09:00:00', 'Desktop'),
(3, 2, '2024-03-12 10:00:00', 'Smart Speaker'),
(4, 3, '2024-03-12 11:00:00', 'Mobile'),
(5, 5, '2024-03-12 12:00:00', 'Desktop');

-- 3. Requêtes de segmentation client

-- Segmentation par tranche d'âge et genre préféré
SELECT
    u.age_group,
    u.preferred_genre,
    COUNT(DISTINCT u.user_id) AS number_of_users
FROM
    users u
GROUP BY
    u.age_group, u.preferred_genre
ORDER BY
    u.age_group, number_of_users DESC;

-- Segmentation par plan d'abonnement et fréquence d'écoute
SELECT
    u.subscription_plan,
    u.listening_frequency,
    COUNT(DISTINCT u.user_id) AS number_of_users
FROM
    users u
GROUP BY
    u.subscription_plan, u.listening_frequency
ORDER BY
    u.subscription_plan, number_of_users DESC;

-- Top 5 des musiques écoutées par les utilisateurs Premium de 20-35 ans
SELECT
    t.track_title,
    t.artist_name,
    COUNT(lh.track_id) AS total_listens
FROM
    listening_history lh
JOIN
    users u ON lh.user_id = u.user_id
JOIN
    tracks t ON lh.track_id = t.track_id
WHERE
    u.age_group = '20-35' AND u.subscription_plan = 'Premium'
GROUP BY
    t.track_title, t.artist_name
ORDER BY
    total_listens DESC
LIMIT 5;

-- Genres les plus populaires par tranche d'âge
SELECT
    u.age_group,
    u.preferred_genre,
    COUNT(u.preferred_genre) AS genre_count
FROM
    users u
GROUP BY
    u.age_group, u.preferred_genre
ORDER BY
    u.age_group, genre_count DESC;

-- Utilisateurs qui écoutent les Top 10 musiques et leur comportement
SELECT
    u.user_id,
    u.age_group,
    u.gender,
    u.subscription_plan,
    t.track_title,
    t.artist_name,
    lh.listen_date
FROM
    listening_history lh
JOIN
    users u ON lh.user_id = u.user_id
JOIN
    tracks t ON lh.track_id = t.track_id
WHERE
    t.track_id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) -- IDs des Top 10 musiques
ORDER BY
    u.user_id, lh.listen_date DESC;
