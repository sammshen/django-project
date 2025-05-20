import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

hash_set = set(hashes)

# The absolute most common words in English
TOP_WORDS = ["the", "of", "and", "a", "to", "in", "is"]

def check_single_key(key_str):
    """Check if a key can decode any of the top words."""
    matches = []
    key_bytes = key_str.encode("utf-8")

    for word in TOP_WORDS:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hash_set:
            matches.append(word)

    return matches

def worker(start, end, result_queue, progress_queue, worker_id):
    processed = 0

    for i in range(start, end):
        processed += 1
        if processed % 100000 == 0:
            progress_queue.put((worker_id, processed))

        key = f"{i:09d}"  # Format as 9 digits with padding
        matches = check_single_key(key)

        if matches:  # If we found any matches
            result_queue.put((key, matches))
            print(f"Worker {worker_id}: Key {key} matches: {', '.join(matches)}")

def main():
    # Parse range
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        start_range = 0
        end_range = 100000000  # Default: first 100 million

    print(f"Searching for keys from {start_range:,} to {end_range:,}")
    print(f"Looking for matches with: {', '.join(TOP_WORDS)}")

    # Set up multiprocessing
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} CPU cores")

    # Create queues for communication
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
            target=worker,
            args=(chunk_start, chunk_end, result_queue, progress_queue, i)
        )
        processes.append(p)
        p.start()

    # Track results and progress
    found_keys = []
    progress = [0] * num_processes

    try:
        while any(p.is_alive() for p in processes):
            # Process results
            while not result_queue.empty():
                key, words = result_queue.get(block=False)
                found_keys.append((key, words))

            # Update progress
            while not progress_queue.empty():
                worker_id, count = progress_queue.get(block=False)
                progress[worker_id] = count

            # Display progress
            total_checked = sum(progress)
            elapsed = time.time() - start_time
            keys_per_sec = total_checked / elapsed if elapsed > 0 else 0
            percent_done = total_checked / (end_range - start_range) * 100

            print(f"\rProgress: {percent_done:.2f}% | {keys_per_sec:.0f} keys/sec | " +
                  f"Found: {len(found_keys)} matching keys | " +
                  f"Checked: {total_checked:,}", end="")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSearch interrupted. Stopping workers...")
        for p in processes:
            p.terminate()

    # Wait for processes to finish
    for p in processes:
        p.join()

    print("\n\nSearch complete!")

    # Display results
    if found_keys:
        print(f"\nFound {len(found_keys)} keys with matches:")

        # Sort by number of matches, most matches first
        found_keys.sort(key=lambda x: len(x[1]), reverse=True)

        for key, words in found_keys[:20]:  # Show top 20 results
            print(f"Key: {key} - Matches: {', '.join(words)}")

        # Save results to file
        with open("matching_keys.txt", "w") as f:
            f.write(f"Found {len(found_keys)} keys with matches:\n\n")
            for key, words in found_keys:
                f.write(f"Key: {key} - Matches: {', '.join(words)}\n")

        print("\nAll results saved to matching_keys.txt")
    else:
        print("No matching keys found in the specified range.")

if __name__ == "__main__":
    main()