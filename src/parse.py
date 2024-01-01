import requests

from bs4 import BeautifulSoup


def get_bugs_playlist(url):
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    songs = []
    for row in soup.select(".trackList tbody tr"):
        title = row.select_one("th p.title a")
        artist = row.select_one("td.left p.artist a")
        album = row.select_one("td.left a.album")

        if title and artist and album:
            title = title.text.strip()
            artist = artist.text.strip()
            album = album.text.strip()

        songs.append((title, artist, album))

    return songs
