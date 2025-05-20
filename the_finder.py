import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

hash_set = set(hashes)

# Focus solely on "the" - the most common word in English
TARGET_WORD = "the"
TARGET_WORD_BYTES = TARGET_WORD.encode("utf-8")

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys, focusing only on 'the'."""
    processed = 0
    for key_int in range(start, end):
        processed += 1
        if processed % 1000000 == 0:  # Report less frequently for speed
            progress_queue.put((worker_id, processed))

        # Format key
        key_str = f"{key_int:09d}"
        key_bytes = key_str.encode("utf-8")

        # Check only for "the"
        word_hash = hashlib.md5(key_bytes + TARGET_WORD_BYTES).hexdigest()
        if word_hash in hash_set:
            result_queue.put(key_str)
            print(f"Worker {worker_id}: Found key {key_str} that matches '{TARGET_WORD}'")

def main():
    # Parse arguments
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 1000000000  # 1 billion

    print(f"Searching for keys from {start_range:,} to {end_range:,}")
    print(f"Looking for keys that match only the word '{TARGET_WORD}'")

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

    # Start worker processes
    for i in range(num_processes):
        chunk_start = start_range + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else end_range

        p = multiprocessing.Process(
            target=worker_process,
            args=(chunk_start, chunk_end, result_queue, progress_queue, i)
        )
        processes.append(p)
        p.start()

    # Track results
    found_keys = []
    progress = [0] * num_processes

    try:
        while any(p.is_alive() for p in processes):
            # Process results
            while not result_queue.empty():
                key = result_queue.get(block=False)
                found_keys.append(key)

            # Update progress
            while not progress_queue.empty():
                worker_id, count = progress_queue.get(block=False)
                progress[worker_id] = count

            # Display progress
            total_done = sum(progress)
            elapsed = time.time() - start_time
            keys_per_sec = total_done / elapsed if elapsed > 0 else 0
            percent_done = total_done / (end_range - start_range) * 100

            print(f"\rProgress: {percent_done:.2f}% | {keys_per_sec:.0f} keys/sec | " +
                  f"Found: {len(found_keys)} keys | " +
                  f"Checked: {total_done:,}", end="")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSearch interrupted by user. Stopping workers...")
        for p in processes:
            p.terminate()

    # Wait for processes to complete
    for p in processes:
        p.join()

    print("\n\nSearch complete!")

    # Display results
    if found_keys:
        print(f"\nFound {len(found_keys)} keys that match '{TARGET_WORD}':")
        for i, key in enumerate(found_keys[:20]):
            print(f"{i+1}. {key}")

        print("\nTo check a key more thoroughly, run:")
        print(f"python ultra_fast_finder.py check <key>")

        # Save to file
        with open("the_keys.txt", "w") as f:
            f.write(f"Found {len(found_keys)} keys that match '{TARGET_WORD}':\n\n")
            for key in found_keys:
                f.write(f"{key}\n")

        print("\nAll keys saved to the_keys.txt")
    else:
        print(f"No keys found that match '{TARGET_WORD}' in the specified range.")

if __name__ == "__main__":
    main()