import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# Make a dict of hash -> index for easy lookup
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# Expected words based on the solved easy puzzle
expected_words = [
    "the", "north", "carolina", "mutual", "life", "insurance", "agent",
    "promised", "to", "fly", "from", "mercy", "to", "other", "side",
    "of", "lake", "superior", "at", "three", "oclock", "two", "days",
    "before", "event", "was", "place", "he", "tacked", "note", "on",
    "door", "his", "little", "yellow", "house"
]

def check_key(key_str):
    """Check how many expected words this key can decode."""
    matches = 0
    key_bytes = key_str.encode("utf-8")

    for word in expected_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            matches += 1

    return matches

def worker(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys."""
    best_count = 0
    best_key = None
    processed = 0

    for key_int in range(start, end):
        processed += 1
        if processed % 10000 == 0:
            progress_queue.put((worker_id, processed))

        key_str = f"{key_int:09d}"
        matches = check_key(key_str)

        if matches > best_count:
            best_count = matches
            best_key = key_str
            result_queue.put((key_str, matches))
            print(f"Worker {worker_id}: Found key {key_str} with {matches} matches")

    return best_key, best_count

def main():
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default: search a subset of the range
        start_range = 0
        end_range = 10000000  # 10 million keys

    print(f"Searching for keys from {start_range} to {end_range}")

    # Set up multiprocessing
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} CPU cores")

    # Create queues
    result_queue = multiprocessing.Queue()
    progress_queue = multiprocessing.Queue()

    # Split the work
    chunk_size = (end_range - start_range) // num_processes
    processes = []

    start_time = time.time()

    # Start workers
    for i in range(num_processes):
        chunk_start = start_range + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else end_range

        p = multiprocessing.Process(
            target=worker,
            args=(chunk_start, chunk_end, result_queue, progress_queue, i)
        )
        processes.append(p)
        p.start()

    # Track results
    best_keys = []
    best_count = 0
    processed_counts = [0] * num_processes

    try:
        while any(p.is_alive() for p in processes):
            # Check for new results
            while not result_queue.empty():
                key, count = result_queue.get(block=False)
                best_keys.append((key, count))
                if count > best_count:
                    best_count = count
                    print(f"\nNew best overall: key={key}, matches={count}")

            # Update progress
            while not progress_queue.empty():
                worker_id, count = progress_queue.get(block=False)
                processed_counts[worker_id] = count

            # Display progress
            total_processed = sum(processed_counts)
            elapsed = time.time() - start_time
            keys_per_sec = total_processed / elapsed if elapsed > 0 else 0
            percent_done = total_processed / (end_range - start_range) * 100

            print(f"\rProgress: {percent_done:.2f}% | {keys_per_sec:.0f} keys/sec | Best: {best_count} matches", end="")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSearch interrupted. Stopping workers...")
        for p in processes:
            p.terminate()

    # Wait for processes
    for p in processes:
        p.join()

    print("\n\nSearch complete!")

    # Display results
    if best_keys:
        best_keys.sort(key=lambda x: x[1], reverse=True)
        print("\nTop 10 keys:")
        for i, (key, count) in enumerate(best_keys[:10]):
            print(f"{i+1}. Key: {key} - {count} matches")
    else:
        print("No promising keys found.")

if __name__ == "__main__":
    main()