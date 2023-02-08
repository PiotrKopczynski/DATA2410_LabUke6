import threading
import time

def tråd1(tall):
    while True:
        print("Tråd 1 kjører, her er tallet: ", tall)
        time.sleep(2)


def tråd2(tall):
    while True:
        print("Tråd 2 kjører, her er tallet: ", tall)
        time.sleep(2)


t1 = threading.Thread(target=tråd1, args=(1,))
t2 = threading.Thread(target=tråd2,args=(2,))
t1.start()
t2.start()