import hashlib
import multiprocessing
import time
import sys

def read_puzzle_file(file_path):
    """Read the hashed puzzle file."""
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

def check_key(key_str, hashes, hash_to_index, expected_words):
    """Check how many expected words a key can decode."""
    key_bytes = key_str.encode("utf-8")
    matches = 0
    matched_words = []

    for word in expected_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            matches += 1
            matched_words.append(word)

    return matches, matched_words

def process_key_range(start, end, hashes, hash_to_index, expected_words, min_matches, result_queue, progress_queue, worker_id):
    """Check a range of keys and report promising ones."""
    best_count = 0
    best_key = None
    best_matched_words = []
    count = 0
    total = end - start

    for key_int in range(start, end):
        count += 1
        if count % 10000 == 0:  # Report progress periodically
            progress_queue.put((worker_id, count, total))

        key_str = f"{key_int:09d}"
        matches, matched_words = check_key(key_str, hashes, hash_to_index, expected_words)

        if matches >= min_matches and matches > best_count:
            best_count = matches
            best_key = key_str
            best_matched_words = matched_words
            result_queue.put((key_str, matches, matched_words))
            print(f"Worker {worker_id}: New best key {key_str} with {matches} matches")

    # Final report
    progress_queue.put((worker_id, count, total))
    return best_key, best_count, best_matched_words

def decode_with_key(key, hashes, hash_to_index):
    """Decode the puzzle using the given key."""
    decoded_words = {}
    key_bytes = key.encode("utf-8")

    # Try with a dictionary file
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            for word in dictionary:
                word = word.strip().lower()
                if 2 <= len(word) <= 15:  # Reasonable word length
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                    if word_hash in hash_to_index:
                        idx = hash_to_index[word_hash]
                        decoded_words[idx] = word
    except FileNotFoundError:
        print("Dictionary file not found, trying with common words only.")

    # Add known words from context
    context_words = [
        "the", "north", "carolina", "mutual", "life", "insurance", "agent",
        "promised", "to", "fly", "from", "mercy", "to", "other", "side",
        "of", "lake", "superior", "at", "three", "oclock", "two", "days",
        "before", "event", "was", "place", "he", "tacked", "note", "on",
        "door", "his", "little", "yellow", "house", "wednesday", "february",
        "I", "will", "take", "off", "and", "away", "my", "own", "wings",
        "please", "forgive", "me", "loved", "you", "all", "signed",
        "robert", "smith", "ins", "1931", "pm", "am", "o'clock", "18th", "3:00"
    ]

    for word in context_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            idx = hash_to_index[word_hash]
            decoded_words[idx] = word

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded_words:
            message.append(decoded_words[i])
        else:
            message.append(f"[UNKNOWN-{i}]")

    # Calculate stats
    decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))

    return decoded_count, message

def main():
    # Read the puzzle file
    puzzle_path = "puzzle/PUZZLE"
    hashes = read_puzzle_file(puzzle_path)
    hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

    # Words we expect in the message based on the easy puzzle
    expected_words = [
        "the", "north", "carolina", "mutual", "life", "insurance", "agent",
        "promised", "to", "fly", "from", "mercy", "to", "other", "side",
        "of", "lake", "superior", "at", "three", "oclock", "two", "days",
        "before", "event", "was", "place", "he", "tacked", "note", "on",
        "door", "his", "little", "yellow", "house", "wednesday", "february",
        "I", "will", "take", "off", "and", "away", "my", "own", "wings",
        "please", "forgive", "me", "loved", "you", "all", "signed",
        "robert", "smith", "ins"
    ]

    # Parse command line arguments
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default: search a subset of the range
        start_range = 0
        end_range = 10000000  # 10 million keys to start

    # Minimum matches to consider a key promising
    min_matches = 3
    if len(sys.argv) > 3:
        min_matches = int(sys.argv[3])

    print(f"Searching for keys from {start_range} to {end_range}")
    print(f"Looking for keys that match at least {min_matches} expected words")

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
            target=process_key_range,
            args=(chunk_start, chunk_end, hashes, hash_to_index, expected_words,
                  min_matches, result_queue, progress_queue, i)
        )
        processes.append(p)
        p.start()

    # Monitor results and progress
    promising_keys = []
    worker_progress = {}
    best_overall_count = 0

    try:
        while any(p.is_alive() for p in processes):
            # Check for new results
            while not result_queue.empty():
                key, count, words = result_queue.get(block=False)
                promising_keys.append((key, count, words))

                if count > best_overall_count:
                    best_overall_count = count
                    print(f"\nNew best overall: key={key}, matches={count}")
                    print(f"Matched words: {', '.join(words)}")

                    # If we have a very promising key, try decoding with it
                    if count >= 5:  # Threshold for attempting full decode
                        print(f"Promising key found. Decoding full message...")
                        decoded_count, message = decode_with_key(key, hashes, hash_to_index)
                        print(f"Decoded {decoded_count}/{len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")
                        print("Partial message:")
                        print(" ".join(message[:30]) + "...")  # Show start of message

                        # Save to file
                        with open(f"decoded_with_{key}.txt", "w") as f:
                            f.write(f"Key: {key}\n\n")
                            f.write(" ".join(message))
                            f.write(f"\n\nDecoded {decoded_count}/{len(hashes)} words")

            # Update progress tracking
            while not progress_queue.empty():
                worker_id, count, total = progress_queue.get(block=False)
                worker_progress[worker_id] = (count, total)

            # Display overall progress
            if worker_progress:
                total_done = sum(count for count, _ in worker_progress.values())
                total_work = sum(total for _, total in worker_progress.values())
                elapsed = time.time() - start_time

                if total_done > 0 and elapsed > 0:
                    keys_per_sec = total_done / elapsed
                    remaining = (total_work - total_done) / keys_per_sec if keys_per_sec > 0 else 0

                    print(f"\rProgress: {total_done:,}/{total_work:,} keys checked "
                          f"({total_done/total_work*100:.2f}%) | "
                          f"{keys_per_sec:.0f} keys/sec | "
                          f"~{remaining/60:.1f} min remaining | "
                          f"Best: {best_overall_count} matches", end="")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSearch interrupted. Stopping workers...")
        for p in processes:
            p.terminate()

    # Wait for processes to complete
    for p in processes:
        p.join()

    print("\n\nSearch complete!")

    # Display results
    if promising_keys:
        promising_keys.sort(key=lambda x: x[1], reverse=True)
        print("\nTop promising keys:")
        for i, (key, count, words) in enumerate(promising_keys[:10]):
            print(f"{i+1}. Key: {key} - {count} matches: {', '.join(words)}")

        # Decode with the best key
        best_key = promising_keys[0][0]
        print(f"\nDecoding full message with best key: {best_key}")
        decoded_count, message = decode_with_key(best_key, hashes, hash_to_index)

        print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")
        print("\nDecoded message:")
        print(" ".join(message))

        # Save final results
        with open(f"final_decoded.txt", "w") as f:
            f.write(f"Key: {best_key}\n\n")
            f.write(" ".join(message))
            f.write(f"\n\nDecoded {decoded_count}/{len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

        print("\nFinal results saved to final_decoded.txt")
    else:
        print("No promising keys found in the range.")

if __name__ == "__main__":
    main()