import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# Convert to a set for faster lookups
hash_set = set(hashes)

# Most frequent words in English text
COMMON_WORDS = [
    "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
    "he", "was", "for", "on", "as", "with", "his", "they", "at", "be",
    "this", "have", "from", "or", "one", "had", "by", "but", "not", "what",
    "all", "were", "we", "when", "your", "can", "said", "there", "use", "an",
    "each", "which", "she", "do", "how", "their", "if", "will", "up", "other"
]

def check_single_key(key_str):
    """Check if a key can decode any common words."""
    matches = 0
    matched_words = []
    key_bytes = key_str.encode("utf-8")

    for word in COMMON_WORDS:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_set:
            matches += 1
            matched_words.append(word)

    return matches, matched_words

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys."""
    best_count = 0
    best_key = None
    processed = 0

    for key_int in range(start, end):
        processed += 1
        if processed % 100000 == 0:
            progress_queue.put((worker_id, processed))

        key_str = f"{key_int:09d}"
        matches, words = check_single_key(key_str)

        if matches >= 2:
            result_queue.put((key_str, matches, words))
            print(f"Worker {worker_id}: Found promising key {key_str} with {matches} matches: {', '.join(words)}")

        if matches > best_count:
            best_count = matches
            best_key = key_str

    return best_key, best_count

def main():
    # Brute force search mode
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range - use smaller chunks for faster feedback
        start_range = 0
        end_range = 10000000  # First 10 million

    print(f"Searching for keys from {start_range:,} to {end_range:,}")

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
    promising_keys = []
    progress = [0] * num_processes

    try:
        while any(p.is_alive() for p in processes):
            # Process results
            while not result_queue.empty():
                key, count, words = result_queue.get(block=False)
                promising_keys.append((key, count, words))

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
                  f"Found: {len(promising_keys)} promising keys | " +
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

    # Sort and display results
    if promising_keys:
        promising_keys.sort(key=lambda x: x[1], reverse=True)
        print("\nTop promising keys:")
        for i, (key, count, words) in enumerate(promising_keys[:10]):
            print(f"{i+1}. Key: {key} - {count} matches: {', '.join(words)}")

        print("\nNext steps: For each promising key, run a more thorough check to decode the message.")
    else:
        print("No promising keys found in the specified range.")

if __name__ == "__main__":
    main()