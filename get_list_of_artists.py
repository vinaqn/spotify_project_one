import os
import time
import csv
from typing import List, Set, Tuple
import requests
from dotenv import load_dotenv

load_dotenv()


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID") 
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
MARKET = os.getenv("SPOTIFY_MARKET") or "US"  # change if you prefer another market
TARGET_COUNT = 100

def get_app_token(client_id: str, client_secret: str) -> str:
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]

def search_artist(token: str, name: str, market: str="US"):
    """Return (artist_name, artist_id) for the best match to `name`."""
    params = {
        "q": f'artist:"{name}"',
        "type": "artist",
        "limit": 5,
        "market": market
    }
    r = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    if r.status_code == 404:
        # Search should not normally 404; treat as no result
        return None
    r.raise_for_status()
    items = r.json().get("artists", {}).get("items", [])
    if not items:
        return None
    # Prefer exact (case-insensitive) name match, else take top result
    for it in items:
        if it.get("name","").lower() == name.lower():
            return (it["name"], it["id"])
    top = items[0]
    return (top["name"], top["id"])

def main():
    token = get_app_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    # Curated, cross-genre seed names (>>100 to ensure we hit 100 unique IDs)
    seed_names = [
        # pop / alt-pop
        "Chappell Roan","Taylor Swift","Olivia Rodrigo","Billie Eilish","Sabrina Carpenter","Tate McRae",
        "Ariana Grande","Dua Lipa","Ed Sheeran","Adele","Beyoncé","Rihanna","SZA","Doja Cat","Nicki Minaj",
        "Katy Perry","Halsey","Lana Del Rey","Miley Cyrus","Demi Lovato","Selena Gomez","Meghan Trainor",
        "The Weeknd","Post Malone","Justin Bieber","Shawn Mendes","Charlie Puth","Sam Smith","Harry Styles",
        "Niall Horan","ZAYN","One Direction","Coldplay","Imagine Dragons","Maroon 5","OneRepublic",
        "The 1975","Arctic Monkeys","The Killers","Glass Animals","The Chainsmokers","David Guetta",
        "Calvin Harris","Avicii","Kygo","Marshmello","Zedd","Skrillex","DJ Snake","Tiësto","ILLENIUM",
        # hip-hop / r&b
        "Drake","Travis Scott","Kendrick Lamar","J. Cole","Future","Metro Boomin","Lil Baby","Lil Durk",
        "21 Savage","Offset","Quavo","Migos","Cardi B","Megan Thee Stallion","A$AP Rocky","Tyler, The Creator",
        "Playboi Carti","Lil Uzi Vert","Yeat","Ice Spice","Jack Harlow","Latto","Doja Cat","SZA",
        # latin / regional mexicano
        "Bad Bunny","J Balvin","Maluma","KAROL G","Shakira","Rauw Alejandro","ROSALÍA","Feid","Anuel AA",
        "Ozuna","Becky G","Anitta","Luis Fonsi","Sebastián Yatra","Camilo","Manuel Turizo","Myke Towers",
        "TINI","Peso Pluma","Grupo Frontera","Eslabon Armado","Fuerza Regida",
        # country / folk / singer-songwriter
        "Morgan Wallen","Luke Combs","Zach Bryan","Chris Stapleton","Kacey Musgraves","Lainey Wilson",
        "Jelly Roll","Kane Brown","Thomas Rhett","Luke Bryan","Carrie Underwood","Miranda Lambert",
        "Eric Church","Keith Urban","Old Dominion","Dan + Shay","Florida Georgia Line","Noah Kahan","Hozier",
        # k-pop
        "BTS","Jung Kook","Jimin","V","RM","SUGA","J-Hope","BLACKPINK","JENNIE","ROSÉ","LISA",
        "TWICE","Stray Kids","NewJeans","IVE","LE SSERAFIM","SEVENTEEN","ENHYPEN","TOMORROW X TOGETHER",
        "ITZY","aespa","NCT 127","NCT DREAM","ATEEZ",
        # indie / alt / rock
        "Mitski","Phoebe Bridgers","boygenius","The National","Florence + The Machine","Tame Impala","Bon Iver",
        "Vampire Weekend","Arcade Fire","Paramore","Fall Out Boy","blink-182","Linkin Park","Nirvana","Pearl Jam",
        "Foo Fighters","Red Hot Chili Peppers","Green Day","Metallica","AC/DC","Guns N' Roses",
        # legacy / icons
        "The Rolling Stones","Queen","The Beatles","Pink Floyd","Led Zeppelin","Fleetwood Mac","ABBA","U2",
        "Radiohead","Depeche Mode","The Cure","David Bowie","Elton John","Madonna","Michael Jackson","Prince",
        "Bruce Springsteen"
    ]

    # Resolve names -> IDs
    results: List[Tuple[str,str]] = []
    seen: Set[str] = set()
    # Make sure Chappell Roan is first
    seed_names = list(dict.fromkeys(seed_names))  # de-dupe but preserve order
    for name in seed_names:
        pair = search_artist(token, name, MARKET)
        if pair and pair[1] not in seen:
            results.append(pair)
            seen.add(pair[1])
        if len(results) >= TARGET_COUNT:
            break
        time.sleep(0.05)  # be gentle

    # Ensure Chappell Roan present regardless
    chappell_id = "7GlBOeep6PqTfFi59PTUUN"
    if chappell_id not in seen:
        results.insert(0, ("Chappell Roan", chappell_id))

    # Save
    with open("artist_ids.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["artist_name","artist_id"])
        for name, aid in results[:TARGET_COUNT]:
            w.writerow([name, aid])

    print(f"Saved artist_ids.csv with {min(len(results), TARGET_COUNT)} artists.")
    # Also print a few to screen
    for name, aid in results[:10]:
        print(name, aid)

if __name__ == "__main__":
    main()