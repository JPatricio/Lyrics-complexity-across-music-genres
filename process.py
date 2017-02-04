import re
import json
import core
import math
import sys

from collections import Counter
from nltk import RegexpTokenizer, PorterStemmer, pos_tag
from nltk.stem import WordNetLemmatizer


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


def has_characters(inputString):
    return bool(re.search(r'[a-zA-Z]', inputString))


def preprocessing(document):
    normalized_string = document.lower().replace("_", "")
    # 1. Tokenize it! This also removes non alphanumeric characters since we're tokenizing words only.
    # tokenizer = RegexpTokenizer(r'\w+')
    from nltk import word_tokenize
    # tokenizer = SpaceTokenizer()
    tokens = word_tokenize(normalized_string)

    # 3. Remove single punctuation marks
    tokens = [word for word in tokens if has_characters(word)]

    # 4. Stemm it!
    # stemmer = PorterStemmer()
    # stemmed_tokens = [stemmer.stem(word) for word in tokens]

    # Lemmatize
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_tokens

"""
Used simple metrics

• VOCABULARY SIZE
    The number of unique words (in english) used in a genre on its 2k most popular songs

• AVERAGE WORD LENGTH
    The mean of the number of letters that each word has in all songs of a genre

• VOCABULARY DIVERSITY
    A measure given by the vocabulary size divided by the total amount of words used.

Used complex metrics

• LEXICAL OVERLAP
    How often repeated lemmas occur in subsequent verses.

• GIVENNESS
    The proportion of single occurrence lemmas.

• TYPE-TOKEN RATION
    The variation of parts of speech types divided by the total number of words.


If you are trying to assess the structural complexity of any given sentence,
then metrics like you suggested are useful, as is measuring the complexity of the syntax tree
or using something like the Flesch-Kincaid metrics.
http://linguistics.stackexchange.com/questions/8800/what-metrics-can-be-used-to-rate-the-complexity-of-an-english-sentence
"""


def voc_size(doc):
    return len(set(doc))


def infer_simple_statistical_measures():
    # Simple statistics
    for genre in core.genres:
        corpus = list()
        print("Making corpus for " + genre)
        with open("tracks/%s_lyrics.txt" % genre, "r") as myfile:
            these_lyrics = ""
            for line in myfile:
                if "---" in line:
                    corpus.append(these_lyrics)
                    these_lyrics = ""
                else:
                    these_lyrics += line


        genre_vocabulary = list()
        i = 0
        lol = 0
        stats_dict = dict(genre=genre, songs={})
        print("Calculating stats...")
        for song in corpus:
            # print("processing song %s of %s" % (i, len(corpus)))

            # Preprocessing step
            preprocessed_song = preprocessing(song)

            if len(preprocessed_song) == 0:
                continue

            # Vocabulary size
            genre_vocabulary.extend(preprocessed_song)
            song_voc_size = voc_size(preprocessed_song)
            #print("Song vocabulary size is %s" % song_voc_size)

            # New word interval
            new_word_interval = len(preprocessed_song) / song_voc_size
            #print("Song new word interval is %s" % new_word_interval)

            # Average word size
            total_chars = 0
            for token in preprocessed_song:
                total_chars += len(token)

            average_word_size = total_chars / len(preprocessed_song)
            #print("Average word size is %s\n" % average_word_size)
            lol += average_word_size
            # Update stats dict
            stats_dict["songs"][i] = dict(vocabulary_size=song_voc_size,
                                          nwi=new_word_interval,
                                          average_word_size=average_word_size)
            i += 1

        # Genre voc size and NWI
        genre_vocabulary_size = voc_size(genre_vocabulary)
        print("Genre vocabulary size is %s" % genre_vocabulary_size)
        genre_new_word_interval = len(genre_vocabulary) / genre_vocabulary_size
        print("Genre new word interval is %s\n" % genre_new_word_interval)
        print("Number of songs %s\n" % len(stats_dict["songs"]))
        stats_dict["vocabulary_size"] = genre_vocabulary_size
        stats_dict["nwi"] = genre_new_word_interval
        stats_dict["average_word_size"] = lol / len(corpus)
        with open("stats/%s.txt" % genre, "a+") as stats_file:
            stats_file.write(json.dumps(stats_dict))


def calculate_complex_metrics():
    # More complex metrics
    for genre in core.genres:
        corpus = list()
        print("Making corpus for " + genre)
        with open("tracks/%s_lyrics.txt" % genre, "r") as myfile:
            these_lyrics = ""
            for line in myfile:
                if "---" in line:
                    corpus.append(these_lyrics)
                    these_lyrics = ""
                else:
                    these_lyrics += line


        genre_vocabulary = list()
        song_count = 0
        lol = 0
        stats_dict = dict(genre=genre, songs={})
        print("Calculating stats...")
        genre_pos_tags = Counter()
        total_lex_overlap = 0
        total_givenness = 0
        total_ttr = 0
        for song in corpus:
            # print("processing song %s of %s" % (i, len(corpus)))
            # Preprocessing step
            preprocessed_song = preprocessing(song)

            if len(preprocessed_song) == 0:
                continue
            # Lexical overlap
            overlap_count = 0
            for i in range(len(preprocessed_song)):
                for j in range(20):
                    if i+j > (len(preprocessed_song)-1):
                        break
                    if preprocessed_song[i] == preprocessed_song[i+j]:
                        overlap_count += 1
                        break
            lexical_overlap = overlap_count
            total_lex_overlap += lexical_overlap

            # Givenness
            lemma_count = Counter(preprocessed_song)
            givenness = len([lemma for lemma in lemma_count if lemma_count[lemma] == 1])
            total_givenness += givenness

            # Type–token ratio
            pos_tags = pos_tag(preprocessed_song)
            tags_count = Counter([x[1] for x in pos_tags])
            #print(tags_count)
            genre_pos_tags = genre_pos_tags + tags_count


            sum_of_numbers = sum(tags_count.values())
            count = len(tags_count)
            mean = sum_of_numbers / count

            x = Counter(dict.fromkeys(tags_count, math.floor(mean)))
            tags_count.subtract(x)

            variance = sum([x**2 for x in tags_count.values()])
            if variance == 0:
                variance = 1
            ttr = (1/variance) * (count**2)

            stats_dict["songs"][song_count] = dict(lexical_overlap=lexical_overlap,
                                                   givenness=givenness,
                                                   ttr=ttr)
            total_ttr += ttr
            song_count += 1

        # Genre stats
        print("Genre lexical overlap %s" % total_lex_overlap)
        print("Genre givenness %s\n" % total_givenness)
        print("Genre ttr %s\n" % total_ttr)
        nsongs = len(stats_dict["songs"])
        print("Number of songs %s\n" % nsongs)
        stats_dict["lexical_overlap"] = total_lex_overlap / nsongs
        stats_dict["givenness"] = total_givenness / nsongs
        stats_dict["ttr"] = total_ttr / nsongs
        with open("stats/complex_%s.txt" % genre, "a+") as stats_file:
            stats_file.write(json.dumps(stats_dict))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        calculate_complex_metrics()
    else:
        infer_simple_statistical_measures()