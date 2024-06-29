import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

# Configuration de l'authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirect_uri='http://localhost:8888/callback',
    scope='playlist-read-private playlist-modify-private'
))

# Fonction pour obtenir les pistes et leurs dates d'ajout
def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Pondérer les pistes en fonction de leur date d'ajout
def weight_tracks(tracks):
    weighted_tracks = []
    now = datetime.datetime.now()
    for item in tracks:
        track = item['track']
        if 'id' in track and 'added_at' in item:
            added_at = datetime.datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            days_since_added = (now - added_at).days
            if days_since_added <= 14: # moins de 2 semaines
                weight = 6
            elif days_since_added <= 30: # moins d'1 mois
                weight = 4
            elif days_since_added <= 120: # moins de 6 mois
                weight = 3
            elif days_since_added <= 365: # moins d'1 an
                weight = 2
            else: # plus d'un an
                weight = 1
            weighted_tracks.extend([track] * weight)
    print(f"Nombre total de pistes pondérées : {len(weighted_tracks)}")
    return weighted_tracks

# Diviser la liste en lots pour ne pas dépasser la limite de l'API
def chunked_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

# Actualiser la playlist existante avec les pistes pondérées
def update_weighted_playlist(tracks, playlist_id):
    track_ids = [track['id'] for track in tracks]
    
    # Effacer les pistes existantes de la playlist
    sp.playlist_replace_items(playlist_id, [])
    print("Suppression des musiques actuelles")
    
    # Diviser les track_ids en lots de 100
    for chunk in chunked_list(track_ids, 100):
        print(f"Ajout de {len(chunk)} pistes à la playlist.")
        sp.playlist_add_items(playlist_id, chunk)

# ID de la playlist d'origine et de la playlist pondérée
original_playlist_id = 'YOUR_ORIGINAL_PLAYLIST_ID'
weighted_playlist_id = 'YOUR_WEIGHTED_PLAYLIST_ID'

# Obtention et pondération des pistes
tracks = get_playlist_tracks(original_playlist_id)
print(f"Nombre de pistes récupérées : {len(tracks)}")
weighted_tracks = weight_tracks(tracks)

# S'assurer que chaque piste est au moins une fois dans la liste pondérée
unique_tracks = {track['track']['id']: track['track'] for track in tracks if 'id' in track['track']}.values()
for track in unique_tracks:
    if track not in weighted_tracks:
        weighted_tracks.append(track)

# Actualisation de la playlist à laquelle on veut ajouter les musiques pondérées
update_weighted_playlist(weighted_tracks, weighted_playlist_id)

print("Playlist pondérée actualisée avec succès!")