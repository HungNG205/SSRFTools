from threading import Thread

def threads(items, worker, max_threads=40):
    threads = []
    for item in items:
        t = Thread(target=worker, args=(item,))
        threads.append(t)
        t.start()
        if len(threads) >= max_threads:
            for jt in threads:
                jt.join()
            threads = []
    for jt in threads:
        jt.join()
