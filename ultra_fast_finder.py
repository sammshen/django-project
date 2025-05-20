import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

hash_set = set(hashes)

# Another extremely common word in English
TARGET_WORD = "a"
TARGET_WORD_BYTES = TARGET_WORD.encode("utf-8")

def process_batch(start, batch_size, result_queue, worker_id):
    """Process a batch of keys at once."""
    matches = []

    # Check each key in this batch
    for offset in range(batch_size):
        key_int = start + offset
        key_str = f"{key_int:09d}"
        key_bytes = key_str.encode("utf-8")

        # Just check this one common word first
        word_hash = hashlib.md5(key_bytes + TARGET_WORD_BYTES).hexdigest()

        if word_hash in hash_set:
            result_queue.put(key_str)
            print(f"Worker {worker_id}: Found key {key_str} that decodes '{TARGET_WORD}'")
            matches.append(key_str)

    return matches

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys in batches."""
    # Use a large batch size for efficiency
    BATCH_SIZE = 10000
    processed = 0

    for batch_start in range(start, end, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, end)
        actual_batch_size = batch_end - batch_start

        # Process this batch
        process_batch(batch_start, actual_batch_size, result_queue, worker_id)

        # Update progress
        processed += actual_batch_size
        if processed % 1000000 == 0:  # Report less frequently for speed
            progress_queue.put((worker_id, processed))

def check_key(key_str):
    """Verify a key by checking it against several common words."""
    common_words = [
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
        "he", "was", "for", "on", "with"
    ]

    print(f"Checking key: {key_str}")
    key_bytes = key_str.encode("utf-8")
    matches = []

    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hash_set:
            matches.append(word)

    print(f"Key {key_str} matches {len(matches)} common words: {', '.join(matches)}")
    return matches

def decode_with_key(key_str):
    """Decode as much of the message as possible using the key."""
    print(f"Decoding with key: {key_str}")
    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # Create hash -> position mapping (much faster lookup)
    hash_to_pos = {h: i for i, h in enumerate(hashes)}

    # First try with common words
    common_words = [
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
        "he", "was", "for", "on", "with", "as", "his", "they", "at", "be",
        "this", "have", "from", "or", "one", "had", "by", "but", "not", "what",
        "all", "were", "we", "when", "your", "can", "said", "there", "use", "an",
        "each", "which", "she", "do", "how", "their", "if", "will", "up", "other"
    ]

    print("Checking with common words...")
    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hash_to_pos:
            pos = hash_to_pos[word_hash]
            decoded[pos] = word

    print(f"Found {len(decoded)} matches with common words.")

    # Try with a larger dictionary if available
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            print("Checking with system dictionary...")

            for idx, word in enumerate(dictionary):
                if idx % 10000 == 0:
                    print(f"Dictionary progress: {idx} words checked, {len(decoded)} matches found", end="\r")

                word = word.strip().lower()
                if len(word) > 1 and len(word) <= 15:  # Skip very short or long words
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                    if word_hash in hash_to_pos and hash_to_pos[word_hash] not in decoded:
                        pos = hash_to_pos[word_hash]
                        decoded[pos] = word
            print()  # Clear progress line
    except FileNotFoundError:
        print("System dictionary not found.")

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append(f"[{i}]")

    # Print results
    print(f"\nDecoded {len(decoded)}/{len(hashes)} words ({len(decoded)/len(hashes)*100:.1f}%)")

    # Print part of the message
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
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Check mode - verify a key
        if len(sys.argv) > 2:
            key = sys.argv[2]
            check_key(key)
            return
        else:
            print("Usage: python ultra_fast_finder.py check <key>")
            return

    if len(sys.argv) > 1 and sys.argv[1] == "decode":
        # Decode mode - full decode with a key
        if len(sys.argv) > 2:
            key = sys.argv[2]
            decode_with_key(key)
            return
        else:
            print("Usage: python ultra_fast_finder.py decode <key>")
            return

    # Search mode - find the key
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 1000000000  # 1 billion

    print(f"ULTRA-FAST searching for keys from {start_range:,} to {end_range:,}")
    print(f"Looking for keys that can decode the word '{TARGET_WORD}'")

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

                # Check each key we find right away
                print(f"\nVerifying key: {key}")
                matches = check_key(key)
                if len(matches) >= 3:
                    print(f"Promising key found: {key} with {len(matches)} matches!")
                    # Optionally, decode right away
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
        print(f"\nFound {len(found_keys)} keys that can decode '{TARGET_WORD}':")
        for i, key in enumerate(found_keys[:20]):
            print(f"{i+1}. {key}")

        print("\nTo check a key more thoroughly, run:")
        print(f"python {sys.argv[0]} check <key>")

        print("\nTo fully decode with a key, run:")
        print(f"python {sys.argv[0]} decode <key>")

        # Save to file
        with open("found_keys.txt", "w") as f:
            f.write(f"Found {len(found_keys)} keys that can decode '{TARGET_WORD}':\n\n")
            for key in found_keys:
                f.write(f"{key}\n")

        print("\nAll keys saved to found_keys.txt")
    else:
        print(f"No keys found that can decode '{TARGET_WORD}' in the specified range.")

if __name__ == "__main__":
    main()