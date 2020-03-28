"""
Search for songs on spotify
"""

import requests
import json
import yaml
import base64
from yaml import Loader
from datetime import datetime, timedelta

SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
TOKEN_ENDPOINT  = "https://accounts.spotify.com/api/token"

def encodeCredentials(id, secret):
    return base64.b64encode(bytes(id + ':' + secret, 'utf-8')).decode('utf-8')

class SpotifyAuth:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._refresh = None
        self._token = None

    def _load_token(self):
        data = {
            'grant_type': 'client_credentials'
        }
        headers = {
            'Authorization': 'Basic {}'.format(encodeCredentials(self.client_id, self.client_secret))
        }
        resp = requests.post(TOKEN_ENDPOINT, headers=headers, verify=True, data=data)

        if resp.status_code != 200:
            raise RuntimeException('Oops')

        respData = resp.json()
        duration = respData['expires_in']
        self._refresh = datetime.now() + timedelta(0, duration)
        self._token = respData['access_token']

    @property
    def token(self):
        if self._refresh is None or datatime.datetime.now() > self._refresh:
            self._load_token()

        return self._token

class Spotify():
    def __init__(self, client_id, client_secret):
        self.auth = SpotifyAuth(client_id, client_secret)

    def makeQuery(self, q):
        return {
            'q': q,
            'type': 'track',
            'limit': 10,
        }

    def search(self, q):
        headers = {
            "Authorization": "Bearer " + self.auth.token,
        }

        query = self.makeQuery(q)

        return requests.get(SEARCH_ENDPOINT, params=query, headers=headers)

    def lookup(self, track_id):
        headers = {
            "Authorization": "Bearer " + self.auth.token,
        }
        params = {
            'id': track_id,
        }
        return requests.get(SEARCH_ENDPOINT, params=params, headers=headers)

    def getLink(self, track):
        return track['external_urls']['spotify']

    def mostPopular(self, trackList):
        mp = trackList[0]
        for t in trackList[1:]:
            if mp['popularity'] < t['popularity']:
                mp = t

        return mp

if __name__ == '__main__':
    import sys
    with open('./spotify.yml') as keyFile:
        config = yaml.load(keyFile, Loader=Loader)
        CLIENT_ID = config['client_id']
        CLIENT_SECRET = config['secret']

    query = " ".join(sys.argv[1:])
    client = Spotify(CLIENT_ID, CLIENT_SECRET)
    resp = client.search(query)
    tracks = resp.json()['tracks']['items']
    print(client.getLink(client.mostPopular(tracks)))
