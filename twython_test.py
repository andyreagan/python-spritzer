from twython import TwythonStreamer
import datetime
import json

from os.path import isdir
from os import mkdir


class MyStreamer(TwythonStreamer):
    tweets = []
    i = 0
    date = datetime.datetime.now()
    if not isdir(date.strftime("raw/%Y-%m-%d")):
        mkdir(date.strftime("raw/%Y-%m-%d"))
    f = open(date.strftime("raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"), "a")
    # f = open(fname,"a")

    def on_success(self, data):
        self.i += 1
        # self.tweets.append(data)
        if datetime.datetime.now().minute > self.date.minute:
            self.date = datetime.datetime.now()
            self.f.close()
            if not isdir(self.date.strftime("raw/%Y-%m-%d")):
                mkdir(self.date.strftime("raw/%Y-%m-%d"))
            self.f = open(self.date.strftime(
                "raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"), "a")
            print("saved {0} tweets".format(self.i))
            self.i = 0

        self.f.write(json.dumps(data))
        self.f.write("\n")

        # if 'text' in data:
        #     print(data['text'])

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()


APP_KEY = os.environ.get("APP_KEY")
APP_SECRET = os.environ.get("APP_SECRET")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET")

if __name__ == "__main__":
    stream = MyStreamer(APP_KEY, APP_SECRET,
                        OAUTH_TOKEN, OAUTH_TOKEN_SECRET,)

    while True:
        try:
            stream.statuses.filter(locations="-180,-90,180,90")
        except:  # noqa:E722
            print("failed for some reason")
