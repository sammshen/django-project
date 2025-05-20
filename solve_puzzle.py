import hashlib
import string
import itertools
import multiprocessing
from collections import defaultdict
import time
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# Make a dict of hash -> index for easy lookup
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# Common English words to try for initial key testing
common_words = [
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people'
]

# Function to check if a key decodes words
def test_key(key_str):
    matches = 0
    key_bytes = key_str.encode("utf-8")

    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            matches += 1

    return matches

# Function to check a range of keys
def check_key_range(start_key, end_key, best_queue, progress_queue, worker_id):
    best_count = 0
    best_key = None
    count = 0
    total = end_key - start_key

    for key_int in range(start_key, end_key):
        count += 1
        if count % 10000 == 0:  # Report progress periodically
            progress_queue.put((worker_id, count, total))

        key_str = "{:09d}".format(key_int)
        matches = test_key(key_str)

        if matches > best_count:
            best_count = matches
            best_key = key_str
            best_queue.put((best_key, best_count))
            print(f"Worker {worker_id}: New best key {best_key} with {best_count} matches")

    # Final report
    progress_queue.put((worker_id, count, total))
    return best_key, best_count

# Function to decode using a specific key
def decode_with_key(key):
    decoded_words = {}
    key_bytes = key.encode("utf-8")

    # Start with our common words
    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            idx = hash_to_index[word_hash]
            decoded_words[idx] = word

    # Add common phrases from the context
    for word in [
        'agent', 'fly', 'from', 'mercy', 'superior', 'lake', 'three', 'oclock',
        'two', 'days', 'before', 'event', 'place', 'note', 'door', 'little',
        'yellow', 'house', 'wednesday', 'february', 'take', 'off', 'away',
        'own', 'wings', 'please', 'forgive', 'loved', 'robert', 'smith',
        'insurance', 'mutual', 'life', 'carolina', 'north', 'promised',
        'side', 'other', 'superior', 'tacked', 'signed', 'ins', 'will'
    ]:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            idx = hash_to_index[word_hash]
            decoded_words[idx] = word

    # Try more comprehensive wordlists
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
        print("Dictionary file not found.")

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded_words:
            message.append(decoded_words[i])
        else:
            message.append("[UNKNOWN:" + str(i) + "]")

    # Print stats
    decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))
    print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

    # Display the message
    print("\nDecoded message:")
    print(" ".join(message))

    # Dump results to file for further analysis
    print("Writing results to decoded_puzzle_message.txt...")
    with open("decoded_puzzle_message.txt", "w") as f:
        f.write(" ".join(message) + "\n\n")
        f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
        f.write("Remaining unknown indices:\n")
        for idx in range(len(hashes)):
            if idx not in decoded_words:
                f.write(f"{idx}: {hashes[idx]}\n")

    return decoded_count, message

def main():
    # Set up multiprocessing
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} CPU cores")

    # You can specify a range to search within, or use command line arguments
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default: search full 9-digit range
        start_range = 0
        end_range = 1000000000

    print(f"Searching keys from {start_range} to {end_range}")

    # Create queues for communication between processes
    best_queue = multiprocessing.Queue()
    progress_queue = multiprocessing.Queue()

    # Split the range into chunks for each process
    chunk_size = (end_range - start_range) // num_processes
    processes = []

    start_time = time.time()

    # Start the worker processes
    for i in range(num_processes):
        chunk_start = start_range + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else end_range

        p = multiprocessing.Process(
            target=check_key_range,
            args=(chunk_start, chunk_end, best_queue, progress_queue, i)
        )
        processes.append(p)
        p.start()

    # Track the best key found so far
    best_key = None
    best_count = 0

    # Dict to track progress of each worker
    worker_progress = {}

    # Periodically check for results and display progress
    try:
        while any(p.is_alive() for p in processes):
            # Check for new best keys
            while not best_queue.empty():
                key, count = best_queue.get(block=False)
                if count > best_count:
                    best_count = count
                    best_key = key
                    print(f"\nNew best overall: key={best_key}, matches={best_count}")

            # Update progress
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
                    print(f"\rProgress: {total_done}/{total_work} keys checked "
                          f"({total_done/total_work*100:.2f}%) | "
                          f"Speed: {keys_per_sec:.0f} keys/sec | "
                          f"Time: {elapsed:.1f}s elapsed, ~{remaining:.1f}s remaining | "
                          f"Best: {best_key} ({best_count} matches)", end="")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping workers...")
        for p in processes:
            p.terminate()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("\n\nSearch complete!")

    if best_key:
        print(f"Best key found: {best_key} with {best_count} matches")

        # Decode the message with the best key
        print(f"\nDecoding message with key: {best_key}")
        decode_with_key(best_key)
    else:
        print("No matching keys found.")

if __name__ == "__main__":
    main()