import requests
import core


"""
Id's left out:
    Comedy = 3
    Children's music = 4
    Holiday = 8
    Opera = 9
    singer/songwriter = 10
    new age = 13
    soundtrack = 16
    dance = 17
    World = 19
    christian & gospel = 22
    Vocal = 23
    Easy listening = 25
    j-pop = 27
    enka = 28
    Anime = 29
    Kayokyoku = 30
    fitness and workout = 50
    karaoke = 52
    instrumental = 53
    Latin urban = 1119
    k-pop = 1614

"""

genre_dict = dict(
    blues=2,
    classical=5,
    country=6,
    eletronic=7,
    jazz=11,
    latin=12,
    pop=14,
    RBSoul=15,
    hiphoprap=18,
    alternative=20,
    rock=21,
    reggae=24,
)
"""
try:
    for genre, genre_id in genre_dict.items():
        page = 1
        with open("tracks/%s.txt" % genre, "a+") as myfile:
            while page <= 20:
                r = requests.get(
                    "%strack.search?f_music_genre_id=%s&page_size=2000&page=%s&s_track_rating=desc&f_has_lyrics=1&f_lyrics_language=en" %
                        (API_url, genre_id, page),
                    params=dict(apikey=apikey))
                data = r.json()
                for track in data['message']['body']['track_list']:
                    #print(track['track']['track_id'])
                    #print(track['track']['primary_genres'])
                    myfile.write("%s\n" % track['track']['track_id'])
                page += 1
        print("%s done!" % genre)
except Exception:
    print("Boom!")


for i in range(60, 100):
    r = requests.get("%strack.search?f_music_genre_id=%s&page_size=1&page=1&s_track_rating=desc" % (API_url, i), params=dict(apikey=apikey))
    data = r.json()
    if len(data['message']['body']['track_list']) > 0:
        print(data['message']['body']['track_list'][0]['track']['primary_genres'])
"""

# For Heavy metal Metallica, Death, Black Sabbath, Megadeth, Slayer, Iron Maiden, Judas Priest, Pantera, Anthrax, Ozzy Osbourne

with open("tracks/heavy_metal.txt", "a+") as myfile:
    for artist in ["Metallica", "Death", "Black Sabbath", "Megadeth", "Slayer", "Iron Maiden", "Judas Priest", "Pantera", "Anthrax", "Ozzy Osbourne"]:
        page = 1
        while page <= 2:
            r = requests.get(
                "%strack.search?f_music_genre_id=%s&page_size=200&page=%s&s_track_rating=desc&f_has_lyrics=1&f_lyrics_language=en" %
                    (core.API_url, artist, page),
                params=dict(apikey=core.apikey))
            data = r.json()
            for track in data['message']['body']['track_list']:
                # print(track['track']['track_id'])
                # print(track['track']['primary_genres'])
                myfile.write("%s\n" % track['track']['track_id'])
            page += 1
