import requests
import nltk
import core


def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]


def get_lyrics():
    for genre in core.genres:
        music_count = 0
        with open("tracks/%s.txt" % genre, "r") as myfile:
            with open("tracks/%s_lyrics1.txt" % genre, "a+") as lyricsfile:
                for line in myfile:
                    line = line.replace("\n", "")
                    # print("The id is \"" + line + "\"")
                    r = requests.get("%strack.lyrics.get?track_id=%s" % (core.API_url, line), params=dict(apikey=core.apikey))
                    data = r.json()
                    # print(data)
                    try:
                        lyrics = data['message']['body']['lyrics']['lyrics_body']
                    except KeyError:
                        print(data)
                        continue

                    lyrics = remove_last_line_from_string(lyrics) + "\n---\n"
                    lyricsfile.write(lyrics)
                    music_count += 1
        print("Extracted %s song lyrics for %s" % (music_count, genre))


if __name__ == "__main__":
    get_lyrics()