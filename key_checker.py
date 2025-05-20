import hashlib
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

def check_key(key_str):
    """Check how many words a key can decode."""
    print(f"Checking key: {key_str}")

    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # First try with common words
    common_words = [
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
        "he", "was", "for", "on", "as", "with", "his", "they", "at", "be",
        "this", "have", "from", "or", "one", "had", "by", "but", "not", "what",
        "all", "were", "we", "when", "your", "can", "said", "there", "use", "an",
        "each", "which", "she", "do", "how", "their", "if", "will", "up", "other",
        "about", "out", "many", "then", "them", "these", "so", "some", "her", "would",
        "i", "me", "my", "could", "no", "yes", "only", "very", "just", "than"
    ]

    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hashes:
            idx = hashes.index(word_hash)
            decoded[idx] = word

    # Print initial results
    print(f"Found {len(decoded)} matches with common words.")

    if decoded:
        # Try system dictionary if available
        try:
            with open('/usr/share/dict/words', 'r') as dictionary:
                print("Checking with system dictionary...")
                for word in dictionary:
                    word = word.strip().lower()
                    if len(word) > 1:
                        word_bytes = word.encode("utf-8")
                        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                        if word_hash in hashes and hashes.index(word_hash) not in decoded:
                            idx = hashes.index(word_hash)
                            decoded[idx] = word
        except FileNotFoundError:
            print("System dictionary not found.")

    # Print results
    print(f"Total decoded: {len(decoded)}/{len(hashes)} words ({len(decoded)/len(hashes)*100:.1f}%)")

    # Reconstruct message
    message = []
    for i in range(len(hashes)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append("[?]")

    # Print the first part of the message
    print("\nPartial message:")
    print(" ".join(message[:20]) + "..." if len(message) > 20 else " ".join(message))

    # Save to file
    with open(f"decoded_{key_str}.txt", "w") as f:
        f.write(f"Key: {key_str}\n")
        f.write(f"Decoded: {len(decoded)}/{len(hashes)} words\n\n")
        f.write("Message:\n")
        f.write(" ".join(message))

    print(f"\nFull results saved to decoded_{key_str}.txt")

    return len(decoded), decoded

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python key_checker.py <key>")
        sys.exit(1)

    key = sys.argv[1]
    check_key(key)