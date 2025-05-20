import hashlib
import multiprocessing
import time
import sys
from itertools import product

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# Convert to a set for faster lookups
hash_set = set(hashes)

# Very common words to check
COMMON_WORDS = [
    "the", "and", "for", "not", "but", "you", "all", "any", "can", "had",
    "her", "was", "one", "our", "out", "day", "get", "has", "him", "his",
    "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy",
    "did", "its", "let", "put", "say", "she", "too", "use", "dad", "mom",
    "a", "i", "it", "in", "of", "to", "is", "on", "he", "my", "at", "by",
    "we", "do", "me", "so", "up", "if", "go", "no", "us", "am", "an",
    # Add some common words specific to many types of text
    "said", "from", "have", "this", "that", "they", "will", "with", "been",
    "what", "when", "were", "your", "them", "then", "than", "time", "like",
    "some", "into", "just", "very", "more", "over", "such", "only", "also"
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
            if matches >= 3:  # Early exit once we find a promising key
                return matches, matched_words

    return matches, matched_words

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys."""
    best_count = 0
    best_key = None
    best_words = []
    processed = 0

    for key_int in range(start, end):
        processed += 1
        if processed % 100000 == 0:  # Report less frequently for better performance
            progress_queue.put((worker_id, processed))

        key_str = f"{key_int:09d}"
        matches, words = check_single_key(key_str)

        if matches >= 3:  # Only report keys that decode at least 3 common words
            result_queue.put((key_str, matches, words))
            print(f"Worker {worker_id}: Found promising key {key_str} with {matches} matches: {', '.join(words)}")

        if matches > best_count:
            best_count = matches
            best_key = key_str
            best_words = words

    # Final report
    return best_key, best_count, best_words

def check_target_key(key_str):
    """Check a specific key thoroughly."""
    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # Try with common words first for a quick check
    for word in COMMON_WORDS:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_set:
            # Find the position of this hash in the original hashes list
            for idx, h in enumerate(hashes):
                if h == word_hash:
                    decoded[idx] = word
                    break

    # Try with a larger set of words if we found any matches
    if decoded:
        try:
            with open('/usr/share/dict/words', 'r') as dictionary:
                for word in dictionary:
                    word = word.strip().lower()
                    if 1 <= len(word) <= 15:  # Skip extremely long words
                        word_bytes = word.encode("utf-8")
                        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                        if word_hash in hash_set:
                            for idx, h in enumerate(hashes):
                                if h == word_hash and idx not in decoded:
                                    decoded[idx] = word
                                    break
        except FileNotFoundError:
            print("Dictionary not found.")

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append(f"[{i}]")

    # Return statistics and message
    return len(decoded), message

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Mode to check a specific key
        if len(sys.argv) > 2:
            key = sys.argv[2]
            print(f"Checking key: {key}")
            count, message = check_target_key(key)
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
        end_range = 10000000  # 10 million keys

    print(f"Fast-searching for keys from {start_range:,} to {end_range:,}")

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

                # Check promising keys more thoroughly
                if count >= 3:
                    print(f"\nThoroughly checking promising key: {key}")
                    decoded_count, message = check_target_key(key)
                    print(f"Decoded {decoded_count}/{len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

                    if decoded_count >= 10:  # Save results if we decoded a significant number
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