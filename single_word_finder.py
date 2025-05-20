import hashlib
import multiprocessing
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hash_list = [line.strip() for line in f.readlines()]

hash_set = set(hash_list)

# The most common word in English by far
TARGET_WORD = "the"

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Search for keys that decode the target word."""
    processed = 0
    target_word_bytes = TARGET_WORD.encode("utf-8")

    for key_int in range(start, end):
        processed += 1
        if processed % 100000 == 0:
            progress_queue.put((worker_id, processed))

        key_str = f"{key_int:09d}"
        key_bytes = key_str.encode("utf-8")

        # Check if this key can decode our target word
        word_hash = hashlib.md5(key_bytes + target_word_bytes).hexdigest()

        if word_hash in hash_set:
            result_queue.put(key_str)
            print(f"Worker {worker_id}: Found key {key_str} that decodes '{TARGET_WORD}'")

def check_words_with_key(key_str):
    """Check how many words a key can decode."""
    print(f"Checking key: {key_str}")

    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # Create a hash -> position mapping for faster lookups
    hash_to_pos = {h: i for i, h in enumerate(hash_list)}

    # First check with high-frequency words
    common_words = [
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
        "he", "was", "for", "on", "as", "with", "his", "they", "at", "be",
        "this", "have", "from", "or", "one", "had", "by", "but", "not", "what",
        "all", "were", "we", "when", "your", "can", "said", "there", "use", "an",
        "each", "which", "she", "do", "how", "their", "if", "will", "up", "other",
        "about", "out", "many", "then", "them", "these", "so", "some", "her", "would",
        "i", "me", "my", "could", "no", "yes", "only", "very", "just", "than"
    ]

    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hash_to_pos:
            pos = hash_to_pos[word_hash]
            decoded[pos] = word

    # Print initial results
    print(f"Found {len(decoded)} matches with common words.")

    if len(decoded) >= 3:  # If we have several matches, try with a larger dictionary
        try:
            with open('/usr/share/dict/words', 'r') as dictionary:
                print("Checking with system dictionary...")
                line_count = 0
                for word in dictionary:
                    line_count += 1
                    if line_count % 5000 == 0:
                        print(f"Dictionary progress: {line_count} words checked, {len(decoded)} matches found", end="\r")

                    word = word.strip().lower()
                    if len(word) > 1:
                        word_bytes = word.encode("utf-8")
                        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                        if word_hash in hash_to_pos and hash_to_pos[word_hash] not in decoded:
                            pos = hash_to_pos[word_hash]
                            decoded[pos] = word
            print()  # Clear the progress line
        except FileNotFoundError:
            print("System dictionary not found.")

    # Print results
    print(f"Total decoded: {len(decoded)}/{len(hash_list)} words ({len(decoded)/len(hash_list)*100:.1f}%)")

    # Reconstruct message
    message = []
    for i in range(len(hash_list)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append("[?]")

    # Print the first part of the message
    print("\nPartial message:")
    print(" ".join(message[:30]) + "..." if len(message) > 30 else " ".join(message))

    # Save to file
    with open(f"decoded_{key_str}.txt", "w") as f:
        f.write(f"Key: {key_str}\n")
        f.write(f"Decoded: {len(decoded)}/{len(hash_list)} words\n\n")
        f.write("Message:\n")
        f.write(" ".join(message))
        f.write("\n\nDecoded positions:\n")
        for pos in sorted(decoded.keys()):
            f.write(f"{pos}: {decoded[pos]}\n")

    print(f"\nFull results saved to decoded_{key_str}.txt")

    return len(decoded), decoded

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Mode to check a specific key
        if len(sys.argv) > 2:
            key = sys.argv[2]
            check_words_with_key(key)
            return

    # Search mode
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 1000000000  # 1 billion

    print(f"Searching for keys from {start_range:,} to {end_range:,} that decode '{TARGET_WORD}'")

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

                # Immediately check this key thoroughly
                print(f"\nFound a key that decodes '{TARGET_WORD}': {key}")
                check_words_with_key(key)

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

    if found_keys:
        print(f"\nFound {len(found_keys)} keys that decode '{TARGET_WORD}':")
        for key in found_keys:
            print(f"Key: {key}")

        print("\nTo check a key more thoroughly, run:")
        print(f"python {sys.argv[0]} check <key>")
    else:
        print(f"No keys found that decode '{TARGET_WORD}' in the specified range.")

if __name__ == "__main__":
    main()