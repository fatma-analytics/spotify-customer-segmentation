import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Chargement des données
users = pd.read_csv("spotify_users.csv")
tracks = pd.read_csv("spotify_tracks.csv")
history = pd.read_csv("spotify_listening_history.csv")

# Fusion des données pour l'analyse
df = history.merge(users, on='user_id').merge(tracks, on='track_id')

# Couleurs Spotify
SPOTIFY_GREEN = '#1DB954'
SPOTIFY_BLACK = '#121212'
SPOTIFY_DARK_GREY = '#191414'
SPOTIFY_LIGHT_GREY = '#B3B3B3'
WHITE = '#FFFFFF'

# 2. Création des visuels

# A. Répartition par Tranche d'Âge (Bar Chart)
age_dist = users['age_group'].value_counts().reset_index()
age_dist.columns = ['Tranche d\'Âge', 'Nombre d\'Utilisateurs']
fig_age = px.bar(age_dist, x='Tranche d\'Âge', y='Nombre d\'Utilisateurs', 
                 title='Répartition par Tranche d\'Âge',
                 color_discrete_sequence=[SPOTIFY_GREEN])
fig_age.update_layout(plot_bgcolor=SPOTIFY_DARK_GREY, paper_bgcolor=SPOTIFY_DARK_GREY, font_color=WHITE)

# B. Répartition par Plan d'Abonnement (Pie Chart)
sub_dist = users['subscription_plan'].value_counts().reset_index()
sub_dist.columns = ['Plan', 'Nombre']
fig_sub = px.pie(sub_dist, names='Plan', values='Nombre', 
                 title='Répartition des Abonnements',
                 color_discrete_sequence=[SPOTIFY_GREEN, SPOTIFY_LIGHT_GREY])
fig_sub.update_layout(plot_bgcolor=SPOTIFY_DARK_GREY, paper_bgcolor=SPOTIFY_DARK_GREY, font_color=WHITE)

# C. Genres Préférés par Tranche d'Âge (Stacked Bar)
genre_age = users.groupby(['age_group', 'preferred_genre']).size().reset_index(name='Count')
fig_genre = px.bar(genre_age, x='age_group', y='Count', color='preferred_genre',
                   title='Genres Préférés par Tranche d\'Âge',
                   barmode='stack')
fig_genre.update_layout(plot_bgcolor=SPOTIFY_DARK_GREY, paper_bgcolor=SPOTIFY_DARK_GREY, font_color=WHITE)

# D. Mood Dominant (Bar Chart)
mood_dist = users['listening_mood'].value_counts().reset_index()
mood_dist.columns = ['Mood', 'Nombre']
fig_mood = px.bar(mood_dist, x='Mood', y='Nombre', 
                  title='Mood Dominant des Utilisateurs',
                  color_discrete_sequence=[SPOTIFY_GREEN])
fig_mood.update_layout(plot_bgcolor=SPOTIFY_DARK_GREY, paper_bgcolor=SPOTIFY_DARK_GREY, font_color=WHITE)

# E. Top 5 Musiques les plus écoutées
top_tracks = df.groupby(['track_title', 'artist_name']).size().reset_index(name='Écoutes')
top_tracks = top_tracks.sort_values(by='Écoutes', ascending=False).head(5)
fig_top = px.bar(top_tracks, x='Écoutes', y='track_title', orientation='h',
                 title='Top 5 Musiques les plus écoutées',
                 color_discrete_sequence=[SPOTIFY_GREEN],
                 hover_data=['artist_name'])
fig_top.update_layout(plot_bgcolor=SPOTIFY_DARK_GREY, paper_bgcolor=SPOTIFY_DARK_GREY, font_color=WHITE)

# 3. Assemblage du Dashboard HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Spotify Customer Segmentation Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: {SPOTIFY_BLACK};
            color: {WHITE};
            font-family: 'Open Sans', sans-serif;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            font-family: 'Montserrat', sans-serif;
            color: {SPOTIFY_GREEN};
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 30px;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}
        .chart-container {{
            background-color: {SPOTIFY_DARK_GREY};
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #333;
        }}
        .full-width {{
            grid-column: span 2;
        }}
        .kpi-container {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background-color: {SPOTIFY_DARK_GREY};
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            width: 200px;
            border: 1px solid {SPOTIFY_GREEN};
        }}
        .kpi-value {{
            font-size: 32px;
            font-weight: bold;
            color: {SPOTIFY_GREEN};
        }}
        .kpi-label {{
            font-size: 14px;
            color: {SPOTIFY_LIGHT_GREY};
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <h1>Spotify Customer Segmentation Dashboard</h1>
    
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-value">{len(users)}</div>
            <div class="kpi-label">Total Users</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{len(users[users['subscription_plan'] == 'Premium'])}</div>
            <div class="kpi-label">Premium Users</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{len(history)}</div>
            <div class="kpi-label">Total Listens</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{len(tracks)}</div>
            <div class="kpi-label">Tracks Analyzed</div>
        </div>
    </div>

    <div class="dashboard-grid">
        <div class="chart-container">
            {fig_age.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="chart-container">
            {fig_sub.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="chart-container">
            {fig_genre.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="chart-container">
            {fig_mood.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="chart-container full-width">
            {fig_top.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
    </div>
</body>
</html>
"""

with open("spotify_dashboard.html", "w") as f:
    f.write(html_content)

print("Dashboard généré avec succès : spotify_dashboard.html")
