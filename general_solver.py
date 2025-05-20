import hashlib
import multiprocessing
import time
import sys
from collections import Counter

def read_common_words(limit=1000):
    """Read most common English words from the system dictionary."""
    common_words = []
    try:
        with open('/usr/share/dict/words', 'r') as f:
            words = [w.strip().lower() for w in f if 2 <= len(w.strip()) <= 10]
            # Sort by length (preferring shorter common words for testing)
            words.sort(key=len)
            common_words = words[:limit]
    except FileNotFoundError:
        # Fallback to a small list of very common words
        common_words = [
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take'
        ]
    return common_words

def test_key(key_str, hashes, hash_to_index, test_words):
    """Test how many common words a key can decode."""
    key_bytes = key_str.encode("utf-8")
    matches = 0
    matched_words = []

    for word in test_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            matches += 1
            matched_words.append(word)
            # Early exit if we've found enough matches
            if matches >= 5:
                break

    return matches, matched_words

def process_range(start, end, hashes, hash_to_index, test_words, result_queue, progress_queue, worker_id):
    """Process a range of possible keys."""
    best_matches = 0
    best_key = None
    best_words = []
    keys_checked = 0

    for key_num in range(start, end):
        keys_checked += 1
        if keys_checked % 10000 == 0:
            progress_queue.put((worker_id, keys_checked))

        key_str = f"{key_num:09d}"
        matches, words = test_key(key_str, hashes, hash_to_index, test_words)

        if matches > best_matches:
            best_matches = matches
            best_key = key_str
            best_words = words
            result_queue.put((key_str, matches, words))
            print(f"Worker {worker_id}: Found key {key_str} with {matches} matches: {', '.join(words)}")

    return best_key, best_matches, best_words

def decode_message(key, hashes, hash_to_index):
    """Attempt to decode the complete message using a key."""
    key_bytes = key.encode("utf-8")
    decoded = {}

    # First try the system dictionary
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            for word in dictionary:
                word = word.strip().lower()
                if len(word) < 20:  # Skip extremely long words
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                    if word_hash in hash_to_index:
                        idx = hash_to_index[word_hash]
                        decoded[idx] = word
    except FileNotFoundError:
        print("Dictionary not found. Using limited word list.")

    # Try with a list of various common words, numbers, and special terms
    extra_words = [
        # Numbers and dates
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "30", "40", "50", "60", "70", "80", "90", "100", "1000",
        "1st", "2nd", "3rd", "4th", "5th", "10th", "20th",
        "january", "february", "march", "april", "may", "june", "july",
        "august", "september", "october", "november", "december",
        "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
        "mon", "tue", "wed", "thu", "fri", "sat", "sun",

        # Common punctuation and formatting as words
        "mr", "mrs", "ms", "dr", "prof", "jr", "sr", "etc", "e.g", "i.e",
        "a.m", "p.m", "am", "pm", "o'clock", "vs", "etc",

        # Names and titles
        "john", "james", "robert", "mary", "patricia", "jennifer", "michael",
        "william", "david", "richard", "charles", "joseph", "thomas", "smith",
        "johnson", "williams", "jones", "brown", "davis", "miller", "wilson",

        # Various common words not in all dictionaries
        "ok", "okay", "hey", "hi", "hello", "yes", "no", "maybe", "please",
        "thank", "thanks", "sorry", "excuse", "good", "bad", "great", "terrible",
        "sincerely", "regards", "truly", "signed", "signature", "copyright"
    ]

    for word in extra_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            idx = hash_to_index[word_hash]
            decoded[idx] = word

    # Create the message with placeholders for unknown words
    message = []
    for i in range(len(hashes)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append(f"[{i}]")

    decoded_count = len(decoded)
    return decoded_count, message

def main():
    # Read the puzzle file
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

    # Get common words to test
    test_words = read_common_words(1000)
    print(f"Loaded {len(test_words)} common words for testing")

    # Parse command line arguments
    if len(sys.argv) > 2:
        start_range = int(sys.argv[1])
        end_range = int(sys.argv[2])
    else:
        # Default range
        start_range = 0
        end_range = 10000000  # Start with 10M keys

    print(f"Searching for keys from {start_range:,} to {end_range:,}")

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

    # Start workers
    for i in range(num_processes):
        chunk_start = start_range + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else end_range

        p = multiprocessing.Process(
            target=process_range,
            args=(chunk_start, chunk_end, hashes, hash_to_index, test_words,
                  result_queue, progress_queue, i)
        )
        processes.append(p)
        p.start()

    # Monitor progress
    promising_keys = []
    progress_counts = [0] * num_processes
    best_count = 0

    try:
        while any(p.is_alive() for p in processes):
            # Process results
            while not result_queue.empty():
                key, count, words = result_queue.get(block=False)
                promising_keys.append((key, count, words))

                if count > best_count:
                    best_count = count
                    print(f"\nNew best overall: key={key}, matches={count} words: {', '.join(words)}")

                    # Try decoding with promising keys
                    if count >= 4:  # Threshold for attempting full decode
                        print(f"Promising key found. Attempting to decode more...")
                        decoded_count, message = decode_message(key, hashes, hash_to_index)
                        print(f"Decoded {decoded_count}/{len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

                        # Save results
                        filename = f"decoded_with_{key}.txt"
                        with open(filename, "w") as f:
                            f.write(f"Key: {key}\n")
                            f.write(f"Initial matches: {count} ({', '.join(words)})\n")
                            f.write(f"Total decoded: {decoded_count}/{len(hashes)} words\n\n")
                            f.write(" ".join(message))

                        print(f"Results saved to {filename}")

            # Update progress
            while not progress_queue.empty():
                worker_id, count = progress_queue.get(block=False)
                progress_counts[worker_id] = count

            # Display progress
            total_checked = sum(progress_counts)
            elapsed = time.time() - start_time
            keys_per_sec = total_checked / elapsed if elapsed > 0 else 0
            percent_done = total_checked / (end_range - start_range) * 100

            print(f"\rProgress: {percent_done:.2f}% | {keys_per_sec:.0f} keys/sec | " +
                  f"Best: {best_count} matches | Keys checked: {total_checked:,}", end="")

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
    if promising_keys:
        promising_keys.sort(key=lambda x: x[1], reverse=True)
        print("\nTop promising keys:")
        for i, (key, count, words) in enumerate(promising_keys[:10]):
            print(f"{i+1}. Key: {key} - {count} matches: {', '.join(words)}")

        # Decode with the best key
        best_key = promising_keys[0][0]
        print(f"\nFinal decoding with best key: {best_key}")
        decoded_count, message = decode_message(best_key, hashes, hash_to_index)

        print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")
        print("\nPartial message:")
        print(" ".join(message[:50]) + "...")  # Show beginning of message

        # Save final results
        with open("final_decoded.txt", "w") as f:
            f.write(f"Key: {best_key}\n\n")
            f.write(" ".join(message))
            f.write(f"\n\nDecoded {decoded_count}/{len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

        print("\nFinal results saved to final_decoded.txt")
    else:
        print("No promising keys found in the range.")

if __name__ == "__main__":
    main()