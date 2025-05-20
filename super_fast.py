import hashlib
import multiprocessing
import time
import sys
from collections import defaultdict

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hash_list = [line.strip() for line in f.readlines()]

hash_set = set(hash_list)

# Use only a minimal set of extremely high-frequency words for initial checks
MOST_COMMON_WORDS = [
    "the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for"
]

def precompute_hash_parts(word_list, batch_size=10000):
    """Precompute the MD5 parts for words to check multiple keys efficiently."""
    result = {}

    for word in word_list:
        word_bytes = word.encode("utf-8")
        result[word] = word_bytes

    return result

def process_batch(start_key, batch_size, precomputed):
    """Process a batch of keys at once using precomputed word bytes."""
    # Dictionary to store promising keys and their matches
    matches = {}

    # For each key in the batch
    for offset in range(batch_size):
        key_int = start_key + offset
        key_str = f"{key_int:09d}"
        key_bytes = key_str.encode("utf-8")

        # Check each word with this key
        for word, word_bytes in precomputed.items():
            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

            if word_hash in hash_set:
                if key_str not in matches:
                    matches[key_str] = []
                matches[key_str].append(word)

    return matches

def worker_process(start, end, result_queue, progress_queue, worker_id):
    """Process a range of keys in large batches."""
    BATCH_SIZE = 5000  # Process larger batches at once
    processed = 0

    # Precompute hash parts for words
    precomputed = precompute_hash_parts(MOST_COMMON_WORDS)

    for batch_start in range(start, end, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, end)
        actual_batch_size = batch_end - batch_start

        # Process this batch
        batch_matches = process_batch(batch_start, actual_batch_size, precomputed)

        # Report any promising keys
        for key, words in batch_matches.items():
            if len(words) >= 2:  # Only report keys with at least 2 matches
                result_queue.put((key, len(words), words))
                print(f"Worker {worker_id}: Found key {key} with {len(words)} matches: {', '.join(words)}")

        processed += actual_batch_size
        if processed % 100000 == 0:
            progress_queue.put((worker_id, processed))

def check_key_thoroughly(key_str):
    """Check a key with a comprehensive word list."""
    key_bytes = key_str.encode("utf-8")
    decoded = {}
    decoded_positions = {}

    # Create a dictionary of hash -> position for faster lookups
    hash_positions = {h: idx for idx, h in enumerate(hash_list)}

    # First check with common words
    for word in MOST_COMMON_WORDS:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hash_positions:
            pos = hash_positions[word_hash]
            decoded[pos] = word
            decoded_positions[word] = pos

    # Try a larger wordlist
    expanded_words = [
        "about", "after", "all", "also", "am", "an", "another", "any", "are", "as",
        "at", "back", "be", "because", "been", "before", "being", "between", "both",
        "but", "by", "came", "can", "come", "could", "day", "did", "do", "down",
        "each", "even", "first", "from", "get", "give", "go", "had", "has", "have",
        "her", "here", "him", "his", "how", "I", "if", "into", "its", "just",
        "know", "like", "little", "long", "look", "made", "make", "many", "may",
        "me", "might", "more", "most", "much", "must", "my", "never", "new", "no",
        "not", "now", "off", "old", "on", "once", "one", "only", "or", "other",
        "our", "out", "over", "own", "people", "said", "same", "see", "she", "should",
        "so", "some", "such", "take", "than", "that", "their", "them", "then", "there",
        "these", "they", "this", "those", "through", "time", "too", "two", "up", "us",
        "use", "very", "want", "way", "we", "well", "were", "what", "when", "where",
        "which", "who", "will", "with", "would", "year", "your"
    ]

    for word in expanded_words:
        if word not in MOST_COMMON_WORDS:
            word_bytes = word.encode("utf-8")
            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

            if word_hash in hash_positions:
                pos = hash_positions[word_hash]
                if pos not in decoded:
                    decoded[pos] = word
                    decoded_positions[word] = pos

    # Try with a system dictionary if available
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            for line_num, word in enumerate(dictionary):
                if line_num % 1000 == 0:  # Show progress for large dictionaries
                    print(f"Checking dictionary: {line_num} words processed, {len(decoded)} matches found", end="\r")

                word = word.strip().lower()
                if 2 <= len(word) <= 15:  # Skip extremely long or short words
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                    if word_hash in hash_positions:
                        pos = hash_positions[word_hash]
                        if pos not in decoded:
                            decoded[pos] = word
                            decoded_positions[word] = pos
        print()  # Clear the progress line
    except FileNotFoundError:
        print("System dictionary not found, using expanded word list only.")

    # Reconstruct the message
    message = []
    for i in range(len(hash_list)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append(f"[{i}]")

    return len(decoded), message, decoded_positions

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Mode to check a specific key
        if len(sys.argv) > 2:
            key = sys.argv[2]
            print(f"Checking key: {key}")
            count, message, positions = check_key_thoroughly(key)
            print(f"Decoded {count}/{len(hash_list)} words ({count/len(hash_list)*100:.1f}%)")
            print(" ".join(message[:50]) + "...")  # Show beginning of message

            # Save results
            with open(f"decoded_with_{key}.txt", "w") as f:
                f.write(f"Key: {key}\n\n")
                f.write(" ".join(message))
                f.write(f"\n\nDecoded {count}/{len(hash_list)} words ({count/len(hash_list)*100:.1f}%)\n\n")
                f.write("Decoded words and positions:\n")
                for word, pos in sorted(positions.items(), key=lambda x: x[1]):
                    f.write(f"Position {pos}: {word}\n")

            print(f"Results saved to decoded_with_{key}.txt")
            return

    # Brute force search mode
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range - using smaller range for faster results
        start_range = 0
        end_range = 100000000  # 100 million

    print(f"SUPER FAST searching for keys from {start_range:,} to {end_range:,}")

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
                if count >= 2:
                    print(f"\nThoroughly checking promising key: {key}")
                    decoded_count, message, positions = check_key_thoroughly(key)
                    print(f"Decoded {decoded_count}/{len(hash_list)} words ({decoded_count/len(hash_list)*100:.1f}%)")

                    if decoded_count >= 5:  # Save if we found a significant number of matches
                        with open(f"decoded_with_{key}.txt", "w") as f:
                            f.write(f"Key: {key}\n")
                            f.write(f"Initial matches: {count} ({', '.join(words)})\n")
                            f.write(f"Total decoded: {decoded_count}/{len(hash_list)} words\n\n")
                            f.write(" ".join(message))
                            f.write("\n\nDecoded words and positions:\n")
                            for word, pos in sorted(positions.items(), key=lambda x: x[1]):
                                f.write(f"Position {pos}: {word}\n")

                        print(f"Results saved to decoded_with_{key}.txt")

            # Update progress
            while not progress_queue.empty():
                worker_id, count = progress_queue.get(block=False)
                progress[worker_id] = count

            # Display progress
            total_done = sum(progress)
            elapsed = time.time() - start_time
            keys_per_sec = total_done / elapsed if elapsed > 0 else 0
            percent_done = total_done / (end_range - start_range) * 100 if end_range > start_range else 0

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