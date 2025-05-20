import hashlib
import string
import multiprocessing
import time
import sys
from itertools import combinations

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# Make a dict of hash -> index for easy lookup
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# Words that we expect to appear in the text based on the easy puzzle
expected_words = [
    'the', 'north', 'carolina', 'mutual', 'life', 'insurance', 'agent',
    'promised', 'to', 'fly', 'from', 'mercy', 'to', 'the', 'other', 'side',
    'of', 'lake', 'superior', 'at', 'three', 'oclock', 'two', 'days',
    'before', 'the', 'event', 'was', 'to', 'take', 'place', 'he', 'tacked',
    'a', 'note', 'on', 'the', 'door', 'of', 'his', 'little', 'yellow', 'house',
    'at', 'wednesday', 'the', 'of', 'february', 'I', 'will', 'take', 'off',
    'from', 'mercy', 'and', 'fly', 'away', 'on', 'my', 'own', 'wings',
    'please', 'forgive', 'me', 'I', 'loved', 'you', 'all', 'signed',
    'robert', 'smith', 'ins', 'agent'
]

# Function to check if a key decodes specific expected words
def test_key_with_expected_words(key_str, min_matches=3):
    matches = 0
    matched_words = []
    key_bytes = key_str.encode("utf-8")

    for word in expected_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            matches += 1
            matched_words.append(word)
            if matches >= min_matches:
                return matches, matched_words

    return matches, matched_words

# Function to check a range of keys, focusing on expected words
def check_key_range(start_key, end_key, best_queue, progress_queue, worker_id, min_matches=3):
    best_count = 0
    best_key = None
    count = 0
    total = end_key - start_key

    for key_int in range(start_key, end_key):
        count += 1
        if count % 10000 == 0:  # Report progress periodically
            progress_queue.put((worker_id, count, total))

        key_str = "{:09d}".format(key_int)
        matches, matched_words = test_key_with_expected_words(key_str, min_matches)

        if matches >= min_matches:  # Only consider keys with at least min_matches
            if matches > best_count:
                best_count = matches
                best_key = key_str
                best_queue.put((best_key, best_count, matched_words))
                print(f"Worker {worker_id}: New best key {best_key} with {best_count} matches: {', '.join(matched_words)}")

    # Final report
    progress_queue.put((worker_id, count, total))
    return best_key, best_count

# Function to decode the full message once we have a potential key
def decode_full_message(key):
    print(f"\nDecoding full message with key: {key}")
    decoded_words = {}
    key_bytes = key.encode("utf-8")

    # First try our expected words
    for word in expected_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            idx = hash_to_index[word_hash]
            decoded_words[idx] = word

    # Try to decode with a system dictionary
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            for word in dictionary:
                word = word.strip().lower()
                if 2 <= len(word) <= 15:  # Reasonable word length
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                    if word_hash in hash_to_index:
                        idx = hash_to_index[word_hash]
                        if idx not in decoded_words:
                            decoded_words[idx] = word
    except FileNotFoundError:
        print("Dictionary file not found.")

    # Add common words and variations
    common_words = [
        # Add variations and related words
        '1931', '3:00', 'p.m.', '18th', 'pm', 'am', 'o'clock',
        'signed', 'signature', 'sincerely',
        # Add names and titles
        'mr', 'mrs', 'ms', 'dr', 'rev', 'sr', 'jr'
    ]

    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            idx = hash_to_index[word_hash]
            if idx not in decoded_words:
                decoded_words[idx] = word

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded_words:
            message.append(decoded_words[i])
        else:
            message.append(f"[UNKNOWN:{i}]")

    # Print stats
    decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))
    print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

    # Display the message
    print("\nDecoded message:")
    print(" ".join(message))

    # Write results to file
    filename = f"decoded_with_key_{key}.txt"
    with open(filename, "w") as f:
        f.write(" ".join(message) + "\n\n")
        f.write(f"Key: {key}\n")
        f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
        f.write("Remaining unknown indices:\n")
        for idx in range(len(hashes)):
            if idx not in decoded_words:
                f.write(f"{idx}: {hashes[idx]}\n")

    print(f"\nResults saved to {filename}")
    return decoded_count, message

def main():
    # Parse command line arguments
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 1000000000  # All 9-digit numbers

    # Set minimum number of expected word matches to be considered promising
    min_matches = 3
    if len(sys.argv) > 3:
        min_matches = int(sys.argv[3])

    print(f"Searching for keys from {start_range} to {end_range}")
    print(f"Looking for keys that match at least {min_matches} expected words")

    # Set up multiprocessing
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} CPU cores")

    # Create communication queues
    best_queue = multiprocessing.Queue()
    progress_queue = multiprocessing.Queue()

    # Split the work into chunks
    chunk_size = (end_range - start_range) // num_processes
    processes = []

    start_time = time.time()

    # Start worker processes
    for i in range(num_processes):
        chunk_start = start_range + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else end_range

        p = multiprocessing.Process(
            target=check_key_range,
            args=(chunk_start, chunk_end, best_queue, progress_queue, i, min_matches)
        )
        processes.append(p)
        p.start()

    # Track best results and progress
    best_keys = []  # Track all promising keys
    best_count = 0
    worker_progress = {}

    try:
        while any(p.is_alive() for p in processes):
            # Process results from workers
            while not best_queue.empty():
                key, count, matched_words = best_queue.get(block=False)
                best_keys.append((key, count, matched_words))
                if count > best_count:
                    best_count = count
                    print(f"\nNew best overall: key={key}, matches={count} words: {', '.join(matched_words)}")

                    # If we find a key with enough matches, try decoding the full message
                    if count >= 5:  # Threshold for attempting full decode
                        print(f"Found promising key with {count} matches. Attempting full decode...")
                        decode_full_message(key)

            # Update progress tracking
            while not progress_queue.empty():
                worker_id, count, total = progress_queue.get(block=False)
                worker_progress[worker_id] = (count, total)

            # Display progress
            if worker_progress:
                total_done = sum(count for count, _ in worker_progress.values())
                total_work = sum(total for _, total in worker_progress.values())
                elapsed = time.time() - start_time
                if total_done > 0 and elapsed > 0:
                    keys_per_sec = total_done / elapsed
                    remaining = (total_work - total_done) / keys_per_sec if keys_per_sec > 0 else 0
                    print(f"\rProgress: {total_done}/{total_work} keys checked "
                          f"({total_done/total_work*100:.2f}%) | "
                          f"Speed: {keys_per_sec:.0f} keys/sec | "
                          f"Time: {elapsed:.1f}s elapsed, ~{remaining:.1f}s remaining | "
                          f"Best: {best_count} matches", end="")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping workers...")
        for p in processes:
            p.terminate()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("\n\nSearch complete!")

    # Sort and display the best keys
    if best_keys:
        best_keys.sort(key=lambda x: x[1], reverse=True)
        print(f"\nTop 10 most promising keys:")
        for i, (key, count, words) in enumerate(best_keys[:10]):
            print(f"{i+1}. Key: {key} - {count} matches: {', '.join(words)}")

        # Decode with the best key
        best_key = best_keys[0][0]
        print(f"\nDecoding with the best key found: {best_key}")
        decode_full_message(best_key)
    else:
        print("No promising keys found.")

if __name__ == "__main__":
    main()