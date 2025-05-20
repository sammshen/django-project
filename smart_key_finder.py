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

# Extremely common words in English that are likely to appear in most texts
COMMON_WORDS = [
    # Top 25 most common English words
    "the", "of", "and", "to", "a", "in", "that", "it", "is", "was",
    "for", "on", "with", "as", "by", "at", "from", "be", "have", "or",
    "had", "this", "not", "but", "what", "all", "were", "when", "we", "there",
    "can", "an", "your", "which", "their", "said", "if", "will", "one", "about",
    "up", "out", "so", "into", "than", "them", "he", "she", "him", "his",
    "her", "they", "who", "you", "now", "more", "no", "my", "me", "man",
    "our", "other", "only", "do", "has", "more", "time", "some", "would",

    # Based on the PUZZLE-EASY solution which contained a quote from Song of Solomon
    # by Toni Morrison, let's include literary-specific words
    "life", "love", "death", "soul", "heart", "mind", "spirit", "god", "good", "evil",
    "truth", "beauty", "nature", "book", "story", "chapter", "poem", "song", "verse",
    "author", "read", "write", "word", "page", "line", "character", "novel", "poem",

    # Words from the PUZZLE-EASY solution about flying
    "fly", "flew", "flight", "wing", "wings", "air", "sky", "plane", "airplane",
    "bird", "soar", "door", "note", "take", "off", "away", "forgive", "loved",
    "agent", "insurance", "promise", "promised", "mercy", "lake", "superior",
    "february", "robert", "smith", "yellow", "house", "signed", "tacked",
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
            # Early exit for efficiency once we find a promising key
            if matches >= 3:
                break

    return matches, matched_words

def generate_potential_keys():
    """Generate potential keys to try based on some assumptions."""
    # Based on the fact that the easier puzzle used a 4-digit key "6346"
    # Let's try some common patterns and variations
    potential_keys = []

    # Try simple number sequences and popular patterns
    for i in range(10000):
        potential_keys.append(f"{i:09d}")  # 000000000 to 000009999

    # Try dates in format YYYYMMDD - common in passwords
    for year in range(1900, 2023):
        for month in range(1, 13):
            for day in range(1, 32):
                # Skip invalid dates
                if month in [4, 6, 9, 11] and day > 30:
                    continue
                if month == 2 and day > 29:
                    continue
                potential_keys.append(f"{year}{month:02d}{day:02d}")

    # Try repeating numbers like 123123123, 111222333, etc.
    for i in range(1000):
        digits = str(i).zfill(3)
        potential_keys.append(digits * 3)  # repeating pattern three times

    # Try years with padding, e.g., 000001931 (from PUZZLE-EASY)
    for year in range(1900, 2023):
        potential_keys.append(f"00000{year}")

    # Try dates related to Toni Morrison or "Song of Solomon"
    # Publication year of Song of Solomon: 1977
    # Toni Morrison's birth and death years
    special_years = [1931, 1977, 1993, 2019]
    for year in special_years:
        potential_keys.append(f"00000{year}")
        potential_keys.append(f"{year}00000")
        potential_keys.append(f"{year}{year}")

    # Add other potentially relevant key patterns here

    return potential_keys

def worker_process(keys, result_queue, progress_queue, worker_id):
    """Process a subset of keys."""
    best_count = 0
    best_key = None
    best_words = []
    processed = 0
    total_keys = len(keys)

    for key_str in keys:
        processed += 1
        if processed % 1000 == 0:
            progress_queue.put((worker_id, processed, total_keys))

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
            print("Dictionary not found, trying literary word list...")
            # Generate a literary wordlist with additional words
            literary_words = [
                # Literary terms and common words in literary works
                "novel", "poem", "poetry", "story", "fiction", "nonfiction", "character",
                "plot", "setting", "theme", "conflict", "resolution", "climax", "protagonist",
                "antagonist", "narrator", "dialogue", "metaphor", "simile", "imagery", "symbolism",
                "irony", "foreshadowing", "flashback", "allusion", "allegory", "personification",
                "rhyme", "rhythm", "meter", "sonnet", "stanza", "verse", "prose", "tragedy",
                "comedy", "drama", "epic", "memoir", "autobiography", "biography", "journal",
                "letter", "essay", "article", "chapter", "paragraph", "sentence", "word",

                # Words common in literary contexts
                "life", "death", "love", "hate", "joy", "sorrow", "pain", "pleasure", "peace",
                "war", "good", "evil", "truth", "lies", "beauty", "ugliness", "light", "dark",
                "sun", "moon", "stars", "heaven", "hell", "god", "devil", "angel", "demon",
                "spirit", "soul", "mind", "heart", "body", "nature", "earth", "water", "fire",
                "air", "mountain", "river", "sea", "ocean", "forest", "tree", "flower", "bird",
                "animal", "human", "man", "woman", "child", "family", "friend", "enemy",
                "journey", "quest", "adventure", "discovery", "knowledge", "wisdom", "folly",
                "dream", "nightmare", "memory", "time", "past", "present", "future", "begin",
                "end", "birth", "live", "die", "grow", "change", "transform", "create", "destroy",

                # Words from Toni Morrison's works (since PUZZLE-EASY was from her work)
                "beloved", "sula", "paradise", "mercy", "jazz", "tar", "baby", "solomon", "flight",
                "song", "freedom", "slavery", "identity", "ancestry", "heritage", "community",
                "trauma", "memory", "relationship", "family", "mother", "father", "son", "daughter",
                "violence", "oppression", "struggle", "survive", "healing", "forgiveness"
            ]

            for word in literary_words:
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

    if len(sys.argv) > 1 and sys.argv[1] == "brute":
        # Brute force mode
        if len(sys.argv) > 3:
            start_range = int(sys.argv[2])
            end_range = int(sys.argv[3])

            print(f"Brute force searching for keys from {start_range:,} to {end_range:,}")

            # Generate sequential keys
            keys = [f"{i:09d}" for i in range(start_range, end_range)]
            potential_keys = keys
        else:
            print("Please provide start and end range for brute force mode")
            print("Example: python smart_key_finder.py brute 0 1000000")
            return
    else:
        # Smart search mode - use potential keys
        print("Smart search mode - trying potential keys")
        potential_keys = generate_potential_keys()

    print(f"Testing {len(potential_keys):,} potential keys")

    # Set up multiprocessing
    num_processes = multiprocessing.cpu_count()
    print(f"Using {num_processes} CPU cores")

    # Create queues
    result_queue = multiprocessing.Queue()
    progress_queue = multiprocessing.Queue()

    # Split the work
    chunk_size = (len(potential_keys) + num_processes - 1) // num_processes
    processes = []

    start_time = time.time()

    # Start worker processes
    for i in range(num_processes):
        chunk_start = i * chunk_size
        chunk_end = min(chunk_start + chunk_size, len(potential_keys))
        chunk_keys = potential_keys[chunk_start:chunk_end]

        if chunk_keys:  # Only start a process if it has work to do
            p = multiprocessing.Process(
                target=worker_process,
                args=(chunk_keys, result_queue, progress_queue, i)
            )
            processes.append(p)
            p.start()

    # Track results
    promising_keys = []
    progress = [(0, 0)] * num_processes  # (processed, total)

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

                    if decoded_count >= 5:  # Save results if we decoded a significant number
                        with open(f"decoded_with_{key}.txt", "w") as f:
                            f.write(f"Key: {key}\n")
                            f.write(f"Initial matches: {count} ({', '.join(words)})\n")
                            f.write(f"Total decoded: {decoded_count}/{len(hashes)} words\n\n")
                            f.write(" ".join(message))

                        print(f"Results saved to decoded_with_{key}.txt")

            # Update progress
            while not progress_queue.empty():
                worker_id, processed, total = progress_queue.get(block=False)
                progress[worker_id] = (processed, total)

            # Display progress
            total_processed = sum(p[0] for p in progress)
            total_to_process = sum(p[1] for p in progress)
            elapsed = time.time() - start_time
            keys_per_sec = total_processed / elapsed if elapsed > 0 else 0
            percent_done = total_processed / total_to_process * 100 if total_to_process > 0 else 0

            print(f"\rProgress: {percent_done:.2f}% | {keys_per_sec:.0f} keys/sec | " +
                  f"Found: {len(promising_keys)} promising keys | " +
                  f"Checked: {total_processed:,}/{total_to_process:,}", end="")

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