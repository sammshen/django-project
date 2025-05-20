import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

hash_set = set(hashes)

# Common words including many that appear in literary passages
COMMON_WORDS = [
    # Top general words
    "the", "of", "and", "a", "to", "in", "is", "that", "it", "for",
    "was", "on", "are", "as", "with", "his", "they", "at", "be", "this",
    "have", "from", "or", "had", "by", "not", "but", "what", "all", "were",
    "we", "when", "your", "can", "said", "there", "use", "an", "each", "which",

    # Literary/narrative words
    "he", "she", "him", "her", "man", "woman", "life", "death", "love", "heart",
    "soul", "mind", "eyes", "face", "hand", "voice", "words", "time", "day", "night",
    "year", "world", "god", "heaven", "earth", "sea", "water", "fire", "air", "sun",
    "moon", "star", "tree", "flower", "house", "door", "room", "way", "road", "path",

    # Additional from Toni Morrison's style (since PUZZLE-EASY used her text)
    "saw", "heard", "felt", "knew", "thought", "came", "went", "made", "did", "done",
    "left", "right", "tell", "know", "look", "see", "hear", "feel", "think", "believe"
]

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys, checking each against all common words."""
    # Pre-compute word bytes for efficiency
    word_bytes_dict = {word: word.encode("utf-8") for word in COMMON_WORDS}

    # Process keys in our range
    processed = 0
    for key_int in range(start, end):
        processed += 1
        if processed % 1000000 == 0:  # Report less frequently for speed
            progress_queue.put((worker_id, processed))

        # Format key
        key_str = f"{key_int:09d}"
        key_bytes = key_str.encode("utf-8")

        # Check all common words for this key
        matches = []
        for word, word_bytes in word_bytes_dict.items():
            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
            if word_hash in hash_set:
                matches.append(word)

                # If we found at least one match, this key is potentially interesting
                if len(matches) == 1:
                    result_queue.put((key_str, matches))

                # If we found multiple matches, this is a promising key
                if len(matches) >= 2:
                    print(f"Worker {worker_id}: PROMISING key {key_str} matches: {', '.join(matches)}")

                # Early exit once we've found enough matches (optimization)
                if len(matches) >= 3:
                    break

def main():
    # Parse arguments
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range - try a smaller range for faster results
        start_range = 0
        end_range = 100000000  # 100 million

    print(f"Searching for keys from {start_range:,} to {end_range:,}")
    print(f"Looking for matches with {len(COMMON_WORDS)} common words")
    print(f"Sample words: {', '.join(COMMON_WORDS[:10])}...")

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
    all_keys = {}  # Dictionary of key -> list of matched words
    promising_keys = []  # Keys with 2+ matches
    progress = [0] * num_processes

    try:
        while any(p.is_alive() for p in processes):
            # Process results
            while not result_queue.empty():
                key, matches = result_queue.get(block=False)

                # Update our results
                if key not in all_keys:
                    all_keys[key] = matches
                else:
                    all_keys[key].extend(matches)

                # Add to promising keys if it has multiple matches
                if len(matches) >= 2 and key not in promising_keys:
                    promising_keys.append((key, matches))

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
                  f"Found: {len(all_keys)} keys ({len(promising_keys)} promising) | " +
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
        # Sort by number of matches
        promising_keys.sort(key=lambda x: len(x[1]), reverse=True)

        print(f"\nFound {len(promising_keys)} promising keys with multiple matches:")
        for i, (key, matches) in enumerate(promising_keys[:20]):  # Show top 20
            print(f"{i+1}. Key: {key} - Matches: {', '.join(matches)}")

        # Save to file
        with open("promising_keys.txt", "w") as f:
            f.write(f"Found {len(promising_keys)} promising keys:\n\n")
            for key, matches in promising_keys:
                f.write(f"Key: {key} - Matches: {', '.join(matches)}\n")

        print("\nPromising keys saved to promising_keys.txt")

        print("\nNext steps:")
        print("1. Choose a promising key")
        print("2. Run: python check_promising.py <key>")
    else:
        print(f"No promising keys found in the specified range.")

if __name__ == "__main__":
    main()