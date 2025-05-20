import hashlib
import multiprocessing
import time
import sys
from collections import Counter

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# Convert to a set for faster lookups
hash_set = set(hashes)

# Very common words in English - focusing on the most frequent words
COMMON_WORDS = [
    # Top most frequent words in English
    "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
    "he", "was", "for", "on", "are", "as", "with", "his", "they", "I",
    "at", "be", "this", "have", "from", "or", "one", "had", "by", "word",
    "but", "not", "what", "all", "were", "we", "when", "your", "can", "said",
    "there", "use", "an", "each", "which", "she", "do", "how", "their", "if",
    "will", "up", "other", "about", "out", "many", "then", "them", "these", "so",
    "some", "her", "would", "make", "like", "him", "into", "time", "has", "look",
    "two", "more", "write", "go", "see", "number", "no", "way", "could", "people"
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
            # Early exit for efficiency once we find enough matches
            if matches >= 3:
                break

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

        # Only report keys that decode multiple common words
        if matches >= 2:
            result_queue.put((key_str, matches, words))
            print(f"Worker {worker_id}: Found promising key {key_str} with {matches} matches: {', '.join(words)}")

        if matches > best_count:
            best_count = matches
            best_key = key_str
            best_words = words

    return best_key, best_count, best_words

def check_target_key(key_str):
    """Check a specific key thoroughly."""
    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # First, try with common words
    for word in COMMON_WORDS:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_set:
            for idx, h in enumerate(hashes):
                if h == word_hash:
                    decoded[idx] = word
                    break

    # Try with a larger word list if we found any matches
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
            print("Dictionary not found, using expanded wordlist...")
            # Use an expanded list of common words
            expanded_words = [
                # Add more common words
                "about", "after", "again", "air", "all", "along", "also", "always", "America",
                "an", "and", "animal", "another", "answer", "any", "are", "around", "as", "ask",
                "at", "away", "back", "be", "because", "been", "before", "began", "begin", "being",
                "below", "between", "big", "book", "both", "boy", "but", "by", "call", "came",
                "can", "car", "carry", "change", "children", "city", "close", "come", "could",
                "country", "cut", "day", "did", "different", "do", "does", "don't", "down",
                "each", "earth", "eat", "end", "enough", "even", "every", "example", "eye",
                "face", "family", "far", "father", "feet", "few", "find", "first", "follow",
                "food", "for", "form", "found", "four", "from", "get", "girl", "give", "go",
                "good", "got", "great", "group", "grow", "had", "hand", "hard", "has", "have",
                "he", "head", "hear", "help", "her", "here", "high", "him", "his", "home",
                "house", "how", "idea", "if", "important", "in", "Indian", "into", "is", "it",
                "its", "it's", "just", "keep", "kind", "know", "land", "large", "last", "later",
                "learn", "leave", "left", "let", "letter", "life", "light", "like", "line",
                "list", "little", "live", "long", "look", "made", "make", "man", "many", "may",
                "me", "mean", "men", "might", "mile", "miss", "more", "most", "mother", "mountain",
                "move", "much", "must", "my", "name", "near", "need", "never", "new", "next",
                "night", "no", "not", "now", "number", "of", "off", "often", "old", "on",
                "once", "one", "only", "open", "or", "other", "our", "out", "over", "own",
                "page", "paper", "part", "people", "picture", "place", "plant", "play", "point",
                "put", "question", "quick", "quickly", "quite", "read", "really", "right", "river",
                "run", "said", "same", "saw", "say", "school", "sea", "second", "see", "seem",
                "sentence", "set", "she", "should", "show", "side", "small", "so", "some",
                "something", "sometimes", "song", "soon", "sound", "spell", "start", "state",
                "still", "stop", "story", "study", "such", "take", "talk", "tell", "than",
                "that", "the", "their", "them", "then", "there", "these", "they", "thing",
                "think", "this", "those", "thought", "three", "through", "time", "to", "together",
                "too", "took", "tree", "try", "turn", "two", "under", "until", "up", "us",
                "use", "very", "walk", "want", "was", "watch", "water", "way", "we", "well",
                "went", "were", "what", "when", "where", "which", "while", "white", "who",
                "why", "will", "with", "without", "word", "work", "world", "would", "write",
                "year", "you", "young", "your"
            ]

            for word in expanded_words:
                word_bytes = word.encode("utf-8")
                word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
                if word_hash in hash_set:
                    for idx, h in enumerate(hashes):
                        if h == word_hash and idx not in decoded:
                            decoded[idx] = word
                            break

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
        # Default range - use smaller chunks for faster feedback
        # We can run this multiple times with different ranges
        start_range = 0
        end_range = 10000000  # Start with the first 10 million

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
                if count >= 2:  # Lower threshold for thorough checking
                    print(f"\nThoroughly checking promising key: {key}")
                    decoded_count, message = check_target_key(key)
                    print(f"Decoded {decoded_count}/{len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

                    if decoded_count >= 3:  # Lower threshold for saving results
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