import requests
from pyscript import window

def urlify(in_string):
    return "%20".join(in_string.split())

class Song:
    def __init__(self, url, name, artists, danceability, energy, key, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo):
        self.url = url
        self.name = name
        self.artists = ", ".join(artists)
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.player = None

    def play(self):
        if self.player is None:
            self.player = window.Audio.new(self.url)
        self.player.play()
        
class Spotify:
    API_URL = "https://pyscript-spotify-api.vercel.app/api"

    def __init__(self):
        self.token = self._get_token()

    def _get_token(self):
        response = requests.get(f"{self.API_URL}/spotify-token")
        data = response.json()
        return f"Bearer {data['token']}"

    def _get_spotify_headers(self):
        return {
            "Authorization": self.token
        }

    def _search_tracks(self, song_name):
        search_url = f"{self.API_URL}/search?name={urlify(song_name)}"
        response = requests.get(search_url, headers=self._get_spotify_headers())
        data = response.json()
        return data.get("tracks", {}).get("items", [])

    def _get_song_features(self, track_id):
        features_url = f"{self.API_URL}/song-features?id={track_id}"
        response = requests.get(features_url, headers=self._get_spotify_headers())
        data = response.json()
        return data

    def get_song(self, song_name):
        tracks = self._search_tracks(song_name)
        if not tracks:
            print("Song not found.")
            return None

        track = tracks[0]
        preview_url = track["preview_url"]

        if preview_url is None:
            print("Song has no preview URL.")
            return None
        
        features = self._get_song_features(track["id"])
        artists = [artist["name"] for artist in track["artists"]]

        song = Song(
            url=preview_url,
            name=track["name"],
            artists=artists,
            danceability=features["danceability"],
            energy=features["energy"],
            key=features["key"],
            loudness=features["loudness"],
            speechiness=features["speechiness"],
            acousticness=features["acousticness"],
            instrumentalness=features["instrumentalness"],
            liveness=features["liveness"],
            valence=features["valence"],
            tempo=features["tempo"]
        )

        return song