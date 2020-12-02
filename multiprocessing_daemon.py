from multiprocessing import Process
from datetime import datetime

from twython import TwythonStreamer
from json import dumps

from os.path import isdir
from os import mkdir

APP_KEY = os.environ.get("APP_KEY")
APP_SECRET = os.environ.get("APP_SECRET")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET")


class MyStreamer(TwythonStreamer):
    tweets = []
    i = 0

    # date = datetime.now()
    # f = open(date.strftime("%Y-%m-%d-%H-%M.json"),"a")
    # f = open(fname,"a")

    # f

    def set_fname(self, fname):
        self.f = open(fname, "a")

    def on_success(self, data):
        # self.i += 1
        # # self.tweets.append(data)
        # if datetime.datetime.now().minute > self.date.minute:
        #     self.date = datetime.datetime.now()
        #     self.f.close()
        #     self.f = open(self.date.strftime("%Y-%m-%d-%H-%M.json"),"a")
        #     print("saved {0} tweets".format(self.i))
        #     self.i = 0

        self.f.write(dumps(data))
        self.f.write("\n")

        # if 'text' in data:
        #     print(data['text'])

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

# bar


def bar():
    # for i in range(100):
    #     print(datetime.now().strftime("%S"))
    #     if datetime.now().strftime("%S") == "00":
    #         raise("process error")
    #     sleep(1)

    date = datetime.now()

    stream = MyStreamer(APP_KEY, APP_SECRET,
                        OAUTH_TOKEN, OAUTH_TOKEN_SECRET,)

    if not isdir(date.strftime("raw/%Y-%m-%d")):
        mkdir(date.strftime("raw/%Y-%m-%d"))
    stream.set_fname(date.strftime("raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"))

    stream.statuses.filter(locations="-180,-90,180,90")


if __name__ == '__main__':
    # Start bar as a process
    p = Process(target=bar)
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(60)

    while True:
        if p.is_alive():
            print("running... let's kill it...")
            # sleep(1)
            # Terminate
            p.terminate()
            p = Process(target=bar)
            p.start()
            p.join(60)
        else:
            print("not running... let's start it")
            p = Process(target=bar)
            p.start()
            p.join(60)
