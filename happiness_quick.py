from datetime import datetime, timedelta
from os.path import isfile, join
from labMTsimple.speedy import sentiDict
from json import loads
from re import findall, UNICODE

LabMT = sentiDict("LabMT", datastructure="dict", stopVal=1.0)


def listify(long_string, lang="en"):
    '''Make a list of words from a string.'''

    replaceStrings = ['---', '--', '\'\'']
    for replaceString in replaceStrings:
        long_string = long_string.replace(replaceString, ' ')
    words = [x.lower() for x in findall(
        r"[\w\@\#\'\&\]\*\-\/\[\=\;]+", long_string, flags=UNICODE)]

    return words


def dictify(something, my_dict, lang="en"):
    '''Take either a list of words or a string, return word dict.

    Pass an empty dict if you want a new one to be made.'''

    # check if it's already a list
    if not type(something) == list:
        something = listify(something, lang=lang)

    for word in something:
        if word in my_dict:
            my_dict[word] += 1
        else:
            my_dict[word] = 1


if __name__ == '__main__':

    f = open("realtime-happs.csv", "r")
    line = ""
    for line in f:
        pass
    f.close()
    leftoff = datetime.strptime(line.rstrip().split(",")[0], "%Y-%m-%d-%H-%M")
    print(leftoff)

    now = datetime.now()
    date = leftoff+timedelta(minutes=1)
    # while we're within the last 15 minutes
    while date < now:
        folder_template = '%Y-%m-%d'
        file_template = '%Y-%m-%d-%H-%M'
        fname = join("raw", folder_template, file_template + ".json")

        print(date.strftime("looking for {}".format(fname)))
        # check that current minute file exists, and next minute

        nextminute = date + timedelta(minutes=1)

        if isfile(date.strftime(fname)) and isfile(nextminute.strftime(fname)):
            print(date.strftime("scoring {}".format(fname)))
            f = open(date.strftime(fname))
            my_dict = dict()
            for line in f:
                tweet = loads(line)
                if 'text' in tweet:
                    dictify(tweet['text'], my_dict)
            f.close()
            happs = LabMT.score(my_dict)
            print(happs)
            f = open("realtime-happs.csv", "a")
            f.write("{0},{1:.6f}\n".format(
                date.strftime("%Y-%m-%d-%H-%M"), happs))
            f.close()

        date += timedelta(minutes=1)
