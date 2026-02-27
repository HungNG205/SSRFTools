from concurrent.futures import ThreadPoolExecutor, as_completed

def run_threads(items, worker, max_threads=40):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(worker, item) for item in items]

        results_count = 0
        for future in as_completed(futures):
            try:
                res = future.result()
                if res:
                    print(res)
                    results_count += 1
            except Exception as e:
                print(f"Thread error: {e}")

        return results_count
