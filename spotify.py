"""
Search for songs on spotify
"""

import requests
import yaml
from yaml import Loader


SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
TOKEN_ENDPOINT  = "https://api.spotify.com/v1/token"

with open('./spotify.yml') as keyFile:
    spotifyConfig = yaml.load(keyFile, Loader=Loader)
    CLIENT_ID = spotifyConfig['client_id']
    CLIENT_SECRET = spotifyConfig['client_secret']

    headers = {
        'Authorization': ""
    }
    TOKEN = requests.post(TOKEN_ENDPOINT)

def makeQuery(q):
    return {
        'q': q,
        'type': 'track',
        'limit': 10,
    }

def search(q):
    headers = {
        "Authorization": "Bearer " + TOKEN,
    }
    return requests.get(SEARCH_ENDPOINT, params=makeQuery(q), headers=headers)

def lookup(track_id):
    headers = {
        "Authorization": "Bearer " + TOKEN,
    }
    params = {
        'id': track_id,
    }
    return requests.get(SEARCH_ENDPOINT, params=params, headers=headers)

def getLink(track):
    return track['external_urls']['spotify']

def mostPopular(trackList):
    mp = trackList[0]
    for t in trackList[1:]:
        if mp['popularity'] < t['popularity']:
            mp = t

    return mp

if __name__ == '__main__':
    import sys

    query = " ".join(sys.argv[1:])
    resp = search(query)
    tracks = resp.json()['tracks']['items']
    print(getLink(mostPopular(tracks)))
