from concurrent.futures import ThreadPoolExecutor, as_completed


def threads(items, worker, max_threads=40):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(worker, item) for item in items]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception:
                pass
