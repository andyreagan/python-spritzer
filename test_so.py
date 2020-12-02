import multiprocessing
import time
import datetime

# bar


def bar():
    for i in range(100):
        print(datetime.datetime.now().strftime("%S"))
        if datetime.datetime.now().strftime("%S") == "00":
            raise("process error")
        time.sleep(1)


if __name__ == '__main__':
    # Start bar as a process
    p = multiprocessing.Process(target=bar)
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(5)

    while True:
        if p.is_alive():
            print("running... let's kill it...")
            time.sleep(1)
            # Terminate
            p.terminate()
            p = multiprocessing.Process(target=bar)
            p.start()
            p.join(5)
        else:
            print("not running... let's start it")
            p = multiprocessing.Process(target=bar)
            p.start()
            p.join(5)
