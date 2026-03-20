from concurrent.futures import ThreadPoolExecutor, as_completed

def run_threads(items, worker, max_threads=40):
    executor = ThreadPoolExecutor(max_workers=max_threads)
    futures = [executor.submit(worker, item) for item in items]

    results_count = 0
    try:
        for future in as_completed(futures):
            try:
                if future.result():
                    results_count += 1
            except Exception as err:
                print(f"Thread error: {err}")
    except KeyboardInterrupt:
        print("\nScan interrupted by user (^C).")
        for future in futures:
            future.cancel()
    finally:
        executor.shutdown(wait=False, cancel_futures=True)

    return results_count
