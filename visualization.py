import json
import core

from scipy.stats import spearmanr, kendalltau, pearsonr, pointbiserialr

stats_dict = dict()

for genre in core.genres:
    # Add 'complex_' before the filename to retrieve complex stats
    with open("stats/complex_%s.txt" % genre, "r") as myfile:
        content = myfile.read()
        stats_dict[genre] = json.loads(content)
        # print("Genre %s has a lexical_overlap of %s" % (genre, stats_dict[genre]["vocabulary_size"]))
        # print(1/stats_dict[genre]["nwi"])


group12 = {"classical": 1, "hiphoprap": 2, "latin": 3, "eletronic": 4,
           "reggae": 5, "jazz": 6, "alternative": 7, "rock":  8,
           "country": 9, "RBSoul": 10, "pop": 11, "blues": 12}
group6 = {"classical": 1,
          "country": 2, "pop": 2, "RBSoul": 2,
          "hiphoprap": 3, "reggae": 3,
          "latin": 4, "eletronic": 4,
          "alternative": 5, "rock": 5,
          "jazz": 6, "blues": 6}
group3 = {"classical": 1,
          "country": 2, "pop": 3, "RBSoul": 3,
          "hiphoprap": 3, "reggae": 3, "latin": 4, "eletronic": 1,
          "alternative": 4, "rock": 4, "jazz": 1, "blues": 1}

result = list()
parameter = list()
for genre in stats_dict:
    i = 0
    if genre == "hiphoprap" or genre == "blues":
        for song in stats_dict[genre]["songs"]:
            # print(stats_dict[genre]["songs"][song])
            parameter.append(stats_dict[genre]["songs"][song]["givenness"])
            result.append(group12[genre])


#group = ["Classical", "Hip", "Latin", "Eletronic", "Reggae", "Jazz", "Alternative", "Rock", "Country", "R&B", "pop", "Blues"]
#group = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#group1 = [0.8201422816,0.6461389175,0.6396928166,0.5329197352,0.4719265275,0.4676430977,0.4627127582,0.3551671704,0.3266560711,0.2340841558,0.2223553007,0.2214475386]

print("....")
print(kendalltau(parameter, result))
print(spearmanr(parameter, result))
print(pearsonr(parameter, result))
print(pointbiserialr(parameter, result))

# print([x for x in parameter if x>9])

import numpy

bins = numpy.linspace(0, 210, 24)
digitized = numpy.digitize(parameter, bins)
# print([x for x in digitized])
# bin_means = [parameter[digitized == i].mean() for i in range(1, len(bins))]
print("------")
print(kendalltau(digitized, result))
print(spearmanr(digitized, result))
print(pearsonr(digitized, result))
print(pointbiserialr(digitized, result))
