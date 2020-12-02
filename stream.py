import datetime
import json
import os
import sys
from os import mkdir
from os.path import isdir

from twython import TwythonStreamer
from requests.exceptions import ChunkedEncodingError

APP_KEY = os.environ.get("APP_KEY")
APP_SECRET = os.environ.get("APP_SECRET")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET")

track = os.environ.get("track", "twitter")
outputfolder = os.environ.get("outputfolder", "test")

BASE_DIR = "/data/"

date = datetime.datetime.now()
if not isdir(date.strftime(BASE_DIR + "raw".format(outputfolder))):
    mkdir(date.strftime(BASE_DIR + "raw".format(outputfolder)))
if not isdir(date.strftime(BASE_DIR + "raw/{}".format(outputfolder))):
    mkdir(date.strftime(BASE_DIR + "raw/{}".format(outputfolder)))
if not isdir(date.strftime(BASE_DIR + "raw/{}/%Y-%m-%d".format(outputfolder))):
    mkdir(date.strftime(BASE_DIR + "raw/{}/%Y-%m-%d".format(outputfolder)))
f = open(date.strftime(BASE_DIR + "raw/{}/%Y-%m-%d/%Y-%m-%d-%H-%M.json".format(outputfolder)), "a")


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        f.write(json.dumps(data))
        f.write("\n")

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

while True:
    try:
        stream.statuses.filter(track=track)
    except ChunkedEncodingError as err:
        print("Streaming error: {0}".format(err))
    except:  # noqa: E722
        print("Unexpected error:", sys.exc_info()[0])
        raise
