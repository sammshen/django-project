import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

hash_set = set(hashes)

# Only use the top 20 most common English words - extremely minimal for max speed
TOP_20_WORDS = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at"
]

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys."""
    processed = 0

    # Pre-compute word bytes (small optimization)
    word_bytes_dict = {word: word.encode("utf-8") for word in TOP_20_WORDS}

    # Process each key in our range
    for key_int in range(start, end):
        # Update progress counter
        processed += 1
        if processed % 1000000 == 0:  # Report less frequently for speed
            progress_queue.put((worker_id, processed))

        # Format key as 9-digit string with leading zeros
        key_str = f"{key_int:09d}"
        key_bytes = key_str.encode("utf-8")

        # Check this key against each word
        matches = []
        for word, word_bytes in word_bytes_dict.items():
            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
            if word_hash in hash_set:
                matches.append(word)

                # Early exit if we found multiple matches (promising key)
                if len(matches) >= 2:
                    result_queue.put((key_str, matches))
                    print(f"Worker {worker_id}: Found key {key_str} with matches: {', '.join(matches)}")
                    break

def decode_with_key(key_str):
    """Decode as much of the message as possible using the key."""
    print(f"Decoding with key: {key_str}")
    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # Create a mapping of hash to position for faster lookups
    hash_to_pos = {h: i for i, h in enumerate(hashes)}

    # First try with our minimal wordlist
    print("Checking with common words...")
    for word in TOP_20_WORDS:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_pos:
            pos = hash_to_pos[word_hash]
            decoded[pos] = word

    # If we found matches, try with a larger wordlist
    if decoded:
        print(f"Found {len(decoded)} matches with common words. Trying expanded wordlist...")

        # Larger set of common words
        expanded_words = [
            "this", "what", "all", "were", "we", "when", "your", "can", "said", "there",
            "use", "an", "each", "which", "she", "how", "their", "if", "will", "up",
            "other", "about", "out", "many", "then", "them", "these", "so", "some", "her",
            "would", "make", "like", "him", "into", "time", "has", "look", "two", "more",
            "write", "go", "see", "number", "no", "way", "could", "people", "my", "than",
            "first", "water", "been", "call", "who", "oil", "its", "now", "find", "long",
            "down", "day", "did", "get", "come", "made", "may", "part", "over", "new"
        ]

        for word in expanded_words:
            if word not in TOP_20_WORDS:  # Skip words we already checked
                word_bytes = word.encode("utf-8")
                word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                if word_hash in hash_to_pos and hash_to_pos[word_hash] not in decoded:
                    decoded[hash_to_pos[word_hash]] = word

        # Try with system dictionary if available
        try:
            with open('/usr/share/dict/words', 'r') as dictionary:
                print("Checking with system dictionary...")
                for idx, word in enumerate(dictionary):
                    if idx % 10000 == 0:
                        print(f"Processed {idx} dictionary words, found {len(decoded)} matches...", end="\r")

                    word = word.strip().lower()
                    if 2 <= len(word) <= 15:  # Skip extremely long or short words
                        word_bytes = word.encode("utf-8")
                        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                        if word_hash in hash_to_pos and hash_to_pos[word_hash] not in decoded:
                            decoded[hash_to_pos[word_hash]] = word
            print() # Clear the progress line
        except FileNotFoundError:
            print("System dictionary not found.")

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append(f"[?]")

    # Print statistics and part of the message
    print(f"\nDecoded {len(decoded)}/{len(hashes)} words ({len(decoded)/len(hashes)*100:.1f}%)")
    print("\nPartial message:")
    print(" ".join(message[:50]) + "..." if len(message) > 50 else " ".join(message))

    # Save to file
    with open(f"decoded_with_{key_str}.txt", "w") as f:
        f.write(f"Key: {key_str}\n")
        f.write(f"Decoded {len(decoded)}/{len(hashes)} words ({len(decoded)/len(hashes)*100:.1f}%)\n\n")
        f.write("Message:\n")
        f.write(" ".join(message))
        f.write("\n\nDecoded positions:\n")
        for pos in sorted(decoded.keys()):
            f.write(f"{pos}: {decoded[pos]}\n")

    print(f"\nFull results saved to decoded_with_{key_str}.txt")

    return decoded

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "decode":
        # Decode mode - use a known key
        if len(sys.argv) > 2:
            key = sys.argv[2]
            decode_with_key(key)
            return
        else:
            print("Usage: python efficient_key_finder.py decode <key>")
            return

    # Search mode - find the key
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 1000000000  # 1 billion

    print(f"Searching for keys from {start_range:,} to {end_range:,}")
    print(f"Using {len(TOP_20_WORDS)} most common words: {', '.join(TOP_20_WORDS[:5])}...")

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
                key, words = result_queue.get(block=False)
                found_keys.append((key, words))

                # Optional: immediately decode with this key
                # print(f"\nTrying to decode with key {key}...")
                # decode_with_key(key)

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
                  f"Found: {len(found_keys)} promising keys | " +
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
    if found_keys:
        found_keys.sort(key=lambda x: len(x[1]), reverse=True)
        print(f"\nFound {len(found_keys)} promising keys:")

        for i, (key, words) in enumerate(found_keys[:10]):
            print(f"{i+1}. Key: {key} - Matches: {', '.join(words)}")

        print("\nTo decode with a key, run:")
        print(f"python {sys.argv[0]} decode <key>")

        # Save results
        with open("promising_keys.txt", "w") as f:
            f.write(f"Found {len(found_keys)} promising keys:\n\n")
            for key, words in found_keys:
                f.write(f"Key: {key} - Matches: {', '.join(words)}\n")

        print("\nAll promising keys saved to promising_keys.txt")
    else:
        print("No promising keys found in the specified range.")

if __name__ == "__main__":
    main()