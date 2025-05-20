import hashlib
from collections import Counter

def load_puzzle():
    """Load the puzzle hashes."""
    with open("puzzle/PUZZLE", "r") as f:
        return [line.strip() for line in f.readlines()]

def identify_repeated_hashes(hashes):
    """Find hashes that appear multiple times and their positions."""
    counts = Counter(hashes)
    repeats = {h: [] for h in counts if counts[h] > 1}

    for i, h in enumerate(hashes):
        if h in repeats:
            repeats[h].append(i)

    return repeats

def find_patterns(hashes, min_length=2):
    """Look for repeating patterns/sequences in the hashes."""
    patterns = {}
    total_hashes = len(hashes)

    # Look for patterns of different lengths
    for pattern_len in range(min_length, min(10, total_hashes // 2)):
        for start in range(total_hashes - pattern_len):
            pattern = tuple(hashes[start:start + pattern_len])

            # Check if this pattern appears elsewhere
            for i in range(start + 1, total_hashes - pattern_len + 1):
                if tuple(hashes[i:i + pattern_len]) == pattern:
                    if pattern not in patterns:
                        patterns[pattern] = [start]
                    if i not in patterns[pattern]:
                        patterns[pattern].append(i)

    return patterns

def test_key_on_repeats(key_str, hashes, repeats):
    """Test if a key decodes repeated hashes to the same word."""
    key_bytes = key_str.encode("utf-8")
    words = {}

    # Try to decode each repeated hash with words from a dictionary
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            for word in dictionary:
                word = word.strip().lower()
                if 2 <= len(word) <= 15:  # Skip very short or long words
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                    if word_hash in repeats:
                        if word_hash not in words:
                            words[word_hash] = []
                        words[word_hash].append(word)
    except FileNotFoundError:
        print("Dictionary file not found.")

    # Check common words for repeats
    common_words = [
        "the", "and", "that", "have", "for", "not", "with", "you", "this",
        "but", "his", "from", "they", "she", "will", "would", "there", "their",
        "what", "about", "which", "when", "make", "like", "time", "just", "know",
        "take", "into", "year", "your", "good", "some", "could", "them", "see",
        "other", "than", "then", "now", "look", "only", "come", "its", "over",
        "think", "also", "back", "after", "use", "two", "how", "our", "work",
        "first", "well", "way", "even", "new", "want", "because", "any", "these",
        "give", "day", "most", "us", "is", "are", "was", "were", "be", "been",
        "being", "do", "does", "did", "had", "has", "have", "can", "could",
        "shall", "should", "may", "might", "must", "am", "is", "are", "was",
        "i", "me", "my", "mine", "we", "us", "our", "ours", "you", "your",
        "yours", "he", "him", "his", "she", "her", "hers", "it", "its", "they",
        "them", "their", "theirs", "a", "an", "the", "and", "but", "or", "so",
        "if", "of", "at", "by", "to", "in", "on", "with", "for", "from", "up",
        "down", "over", "under", "again", "further", "then", "once", "here",
        "there", "all", "any", "both", "each", "few", "more", "most", "other",
        "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
        "too", "very"
    ]

    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in repeats:
            if word_hash not in words:
                words[word_hash] = []
            words[word_hash].append(word)

    # Return results
    return words

def main():
    hashes = load_puzzle()
    print(f"Loaded {len(hashes)} hashes from PUZZLE")

    # Find repeated hashes
    repeats = identify_repeated_hashes(hashes)
    print(f"\nFound {len(repeats)} unique hashes that repeat in the puzzle")

    # Show the repeated hashes and positions
    for hash_val, positions in repeats.items():
        print(f"Hash: {hash_val} appears at positions: {positions}")

    # Look for patterns
    patterns = find_patterns(hashes)
    if patterns:
        print(f"\nFound {len(patterns)} repeating patterns in the hashes")
        for pattern, positions in patterns.items():
            if len(positions) >= 2:  # Only show patterns that appear multiple times
                print(f"Pattern of length {len(pattern)} appears at positions: {positions}")
    else:
        print("\nNo repeating patterns found")

    # If a key is known, test it with the repeats
    known_key = input("\nEnter a key to test (or press Enter to skip): ")
    if known_key:
        words = test_key_on_repeats(known_key, hashes, repeats)

        if words:
            print(f"\nFound possible words for repeated hashes using key {known_key}:")
            for hash_val, word_list in words.items():
                positions = repeats[hash_val]
                print(f"Hash: {hash_val} at positions {positions} could be: {', '.join(word_list)}")
        else:
            print(f"\nNo words found for repeated hashes with key {known_key}")

    # Frequency analysis
    print("\nFrequency analysis of hashes:")
    counts = Counter(hashes)
    most_common = counts.most_common(10)
    for hash_val, count in most_common:
        print(f"Hash: {hash_val} appears {count} times")

    print("\nThis information might help identify common words like 'the', 'and', 'of', etc.")
    print("If certain hashes repeat in patterns similar to English text, that could help find the key.")

if __name__ == "__main__":
    main()