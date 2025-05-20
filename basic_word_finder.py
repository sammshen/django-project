import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

hash_set = set(hashes)

# Basic words found in almost any text
BASIC_WORDS = ["a", "i", "is", "to", "of", "in", "it", "at", "by", "on", "or", "an", "as", "if", "be", "we", "he", "no", "so", "my", "me"]

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys, checking each against basic words."""
    # Pre-compute word bytes for efficiency
    word_bytes_dict = {word: word.encode("utf-8") for word in BASIC_WORDS}

    processed = 0
    for key_int in range(start, end):
        processed += 1
        if processed % 1000000 == 0:  # Report less frequently for speed
            progress_queue.put((worker_id, processed))

        # Format key
        key_str = f"{key_int:09d}"
        key_bytes = key_str.encode("utf-8")

        # Check all basic words for this key
        matches = []
        for word, word_bytes in word_bytes_dict.items():
            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
            if word_hash in hash_set:
                matches.append(word)

                # If we found a match, report it
                if len(matches) == 1:
                    result_queue.put((key_str, matches))

                # If we found multiple matches, this is very promising
                if len(matches) >= 2:
                    print(f"Worker {worker_id}: PROMISING key {key_str} matches: {', '.join(matches)}")

                # Early exit to speed up search once we have enough matches
                if len(matches) >= 3:
                    break

def main():
    # Parse arguments
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 100000000  # 100 million

    print(f"Searching for keys from {start_range:,} to {end_range:,}")
    print(f"Looking for matches with {len(BASIC_WORDS)} basic words: {', '.join(BASIC_WORDS)}")

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
        with open("basic_word_keys.txt", "w") as f:
            f.write(f"Found {len(promising_keys)} promising keys:\n\n")
            for key, matches in promising_keys:
                f.write(f"Key: {key} - Matches: {', '.join(matches)}\n")

        print("\nPromising keys saved to basic_word_keys.txt")

        print("\nNext steps:")
        print("1. Choose a promising key")
        print("2. Run: python ultra_fast_finder.py check <key>")
    else:
        print(f"No promising keys found in the specified range.")

        # At least save any keys with single matches
        if all_keys:
            print(f"\nFound {len(all_keys)} keys with at least one match:")
            sorted_keys = sorted(all_keys.items(), key=lambda x: len(x[1]), reverse=True)
            for i, (key, matches) in enumerate(sorted_keys[:20]):  # Show top 20
                print(f"{i+1}. Key: {key} - Matches: {', '.join(matches)}")

            with open("basic_word_keys.txt", "w") as f:
                f.write(f"Found {len(all_keys)} keys with at least one match:\n\n")
                for key, matches in sorted_keys:
                    f.write(f"Key: {key} - Matches: {', '.join(matches)}\n")

            print("\nAll keys saved to basic_word_keys.txt")

if __name__ == "__main__":
    main()