import hashlib
import multiprocessing
import time
import sys
from collections import defaultdict

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

hash_set = set(hashes)

# We'll focus on a small set of extremely common words for speed
MOST_COMMON_WORDS = [
    "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
    "he", "was", "for", "on", "with", "as", "his", "they", "at", "be"
]

def batch_check(start_key, batch_size):
    """Check a batch of keys at once for any matches."""
    matches = {}

    for word in MOST_COMMON_WORDS:
        word_bytes = word.encode("utf-8")

        # Check each key in the batch
        for offset in range(batch_size):
            key_int = start_key + offset
            key_str = f"{key_int:09d}"
            key_bytes = key_str.encode("utf-8")

            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
            if word_hash in hash_set:
                if key_str not in matches:
                    matches[key_str] = []
                matches[key_str].append(word)

    return matches

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys in batches."""
    BATCH_SIZE = 1000  # Process 1000 keys at a time for efficiency
    processed = 0

    for batch_start in range(start, end, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, end)
        actual_batch_size = batch_end - batch_start

        # Check this batch
        batch_matches = batch_check(batch_start, actual_batch_size)

        # Report promising keys
        for key, words in batch_matches.items():
            if len(words) >= 2:  # Only report keys with multiple matches
                result_queue.put((key, len(words), words))
                print(f"Worker {worker_id}: Found key {key} with {len(words)} matches: {', '.join(words)}")

        processed += actual_batch_size
        if processed % 100000 == 0:
            progress_queue.put((worker_id, processed))

def check_key_thoroughly(key_str):
    """Check a specific key thoroughly with a larger word list."""
    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # First, try with the most common words
    for word in MOST_COMMON_WORDS:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_set:
            for idx, h in enumerate(hashes):
                if h == word_hash:
                    decoded[idx] = word
                    break

    # Try with a larger list
    expanded_words = [
        "about", "after", "all", "also", "an", "because", "but", "by", "can",
        "come", "could", "day", "do", "even", "first", "from", "get", "give", "go",
        "have", "him", "how", "I", "if", "into", "its", "just", "know", "like",
        "look", "make", "me", "most", "my", "new", "no", "not", "now", "one",
        "only", "or", "other", "our", "out", "over", "people", "say", "see", "she",
        "so", "some", "take", "than", "that", "their", "them", "then", "there",
        "these", "they", "think", "this", "time", "two", "up", "us", "use", "want",
        "way", "we", "well", "what", "when", "which", "who", "will", "would", "year"
    ]

    for word in expanded_words:
        if word not in MOST_COMMON_WORDS:  # Skip words we already checked
            word_bytes = word.encode("utf-8")
            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
            if word_hash in hash_set:
                for idx, h in enumerate(hashes):
                    if h == word_hash and idx not in decoded:
                        decoded[idx] = word
                        break

    # Try with system dictionary if available
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            for word in dictionary:
                word = word.strip().lower()
                if 2 <= len(word) <= 15:  # Skip extremely long words
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                    if word_hash in hash_set:
                        for idx, h in enumerate(hashes):
                            if h == word_hash and idx not in decoded:
                                decoded[idx] = word
                                break
    except FileNotFoundError:
        pass  # Dictionary not available

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append(f"[{i}]")

    return len(decoded), message

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Mode to check a specific key
        if len(sys.argv) > 2:
            key = sys.argv[2]
            print(f"Checking key: {key}")
            count, message = check_key_thoroughly(key)
            print(f"Decoded {count}/{len(hashes)} words ({count/len(hashes)*100:.1f}%)")
            print(" ".join(message[:50]) + "...")  # Show beginning of message

            # Save results
            with open(f"decoded_with_{key}.txt", "w") as f:
                f.write(f"Key: {key}\n\n")
                f.write(" ".join(message))
                f.write(f"\n\nDecoded {count}/{len(hashes)} words ({count/len(hashes)*100:.1f}%)")

            print(f"Results saved to decoded_with_{key}.txt")
            return

    # Brute force search mode
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 1000000000  # One billion keys

    print(f"FAST searching for keys from {start_range:,} to {end_range:,}")

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

                # Check promising keys more thoroughly for 3+ matches
                if count >= 2:
                    print(f"\nThoroughly checking promising key: {key}")
                    decoded_count, message = check_key_thoroughly(key)
                    print(f"Decoded {decoded_count}/{len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

                    if decoded_count >= 5:  # Save results if we decoded a significant number
                        with open(f"decoded_with_{key}.txt", "w") as f:
                            f.write(f"Key: {key}\n")
                            f.write(f"Initial matches: {count} ({', '.join(words)})\n")
                            f.write(f"Total decoded: {decoded_count}/{len(hashes)} words\n\n")
                            f.write(" ".join(message))

                        print(f"Results saved to decoded_with_{key}.txt")

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

        print("\nCheck the most promising keys more thoroughly with:")
        print(f"python {sys.argv[0]} check <key>")
    else:
        print("No promising keys found in the specified range.")

if __name__ == "__main__":
    main()