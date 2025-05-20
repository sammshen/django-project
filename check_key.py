import hashlib
import sys

def check_key(key):
    key_str = str(key)
    key_bytes = key_str.encode("utf-8")

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Create a dictionary to store hash -> decoded word mappings
    decoded_words = {}

    print(f"Testing key: {key}")
    print("Attempting to decode puzzle...")

    # First try with common English words
    common_words = [
        "the", "of", "and", "a", "to", "in", "is", "that", "it", "for",
        "was", "on", "are", "as", "with", "his", "they", "at", "be", "this",
        "have", "from", "or", "had", "by", "not", "but", "what", "all", "were",
        "we", "when", "your", "can", "said", "there", "use", "an", "each", "which",
        "she", "do", "how", "their", "if", "will", "up", "other", "about", "out",
        "many", "then", "them", "these", "so", "some", "her", "would", "make", "like",
        "him", "into", "time", "has", "look", "two", "more", "write", "go", "see",
        "number", "no", "way", "could", "people", "my", "than", "first", "water", "been",
        "call", "who", "oil", "its", "now", "find", "long", "down", "day", "did",
        "get", "come", "made", "may", "part", "over", "new", "sound", "take", "only"
    ]

    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hashes:
            decoded_words[word_hash] = word
            print(f"Decoded: {word}")

    # Count matches
    match_count = len(decoded_words)
    total_hashes = len(hashes)

    print(f"\nResults: Matched {match_count} out of {total_hashes} words ({match_count/total_hashes:.1%})")

    # If we decoded at least one word, try reconstructing the text
    if match_count > 0:
        print("\nAttempting to reconstruct text with decoded words:")

        # Print the text with known words and placeholders for unknown
        reconstructed = []
        for h in hashes:
            if h in decoded_words:
                reconstructed.append(decoded_words[h])
            else:
                reconstructed.append("____")

        # Print in chunks of 10 words for readability
        for i in range(0, len(reconstructed), 10):
            print(" ".join(reconstructed[i:i+10]))

    return match_count

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        key = "485066843"  # Default to the key we found

    check_key(key)