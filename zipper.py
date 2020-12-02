from datetime import datetime, timedelta
from os.path import isdir, isfile
from os import mkdir
from subprocess import call

if __name__ == '__main__':
    now = datetime.now()
    date = datetime.now()
    # while we're within the last 15 minutes
    while date > now-timedelta(minutes=100):
        # print(date.strftime("raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"))
        if not isdir(date.strftime("zipped-raw/%Y-%m-%d")):
            mkdir(date.strftime("zipped-raw/%Y-%m-%d"))
        # check that current minute file exists, and next minute
        if isfile(date.strftime("raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json")) and isfile((date+timedelta(minutes=1)).strftime("raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json")):
            print(date.strftime("zipping raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"))
            command = "cat {0} | /usr/local/bin/lz4 -9 > {1}".format(date.strftime(
                "raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"), date.strftime("zipped-raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json.lz4"))
            call(command, shell=True)
            command = "rm {0}".format(date.strftime(
                "raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"))
            call(command, shell=True)
        # or, the next minute file is zipped already
        elif isfile(date.strftime("raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json")) and isfile((date+timedelta(minutes=1)).strftime("zipped-raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json.lz4")):
            print(date.strftime("zipping raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"))
            command = "cat {0} | /usr/local/bin/lz4 -9 > {1}".format(date.strftime(
                "raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"), date.strftime("zipped-raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json.lz4"))
            call(command, shell=True)
            command = "rm {0}".format(date.strftime(
                "raw/%Y-%m-%d/%Y-%m-%d-%H-%M.json"))
            call(command, shell=True)
        date -= timedelta(minutes=1)
