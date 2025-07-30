import time

def test2():
    print("OK")

def test():
    while 1:
        time.sleep(1)
        test2()


if __name__ == "__main__":
    test()
