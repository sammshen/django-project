import hashlib
import sys

# Read the puzzle file
with open("puzzle/PUZZLE", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

def check_key(key_str):
    """Thoroughly check a key against the puzzle."""
    print(f"Checking key: {key_str}")

    key_bytes = key_str.encode("utf-8")
    decoded = {}

    # Try with common English words first
    common_words = [
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
        "he", "was", "for", "on", "as", "with", "his", "they", "at", "be",
        "this", "have", "from", "or", "one", "had", "by", "but", "not", "what",
        "all", "were", "we", "when", "your", "can", "said", "there", "use", "an",
        "each", "which", "she", "do", "how", "their", "if", "will", "up", "other",
        "about", "out", "many", "then", "them", "these", "so", "some", "her", "would",
        "make", "like", "him", "into", "time", "has", "look", "two", "more", "write",
        "go", "see", "number", "no", "way", "could", "people", "my", "than", "first",
        "water", "been", "call", "who", "oil", "its", "now", "find", "long", "down",
        "day", "did", "get", "come", "made", "may", "part", "over", "new", "sound",
        "take", "only", "little", "work", "know", "place", "year", "live", "me", "back",
        "give", "most", "very", "after", "thing", "our", "just", "name", "good", "sentence",
        "man", "think", "say", "great", "where", "help", "through", "much", "before", "line",
        "right", "too", "mean", "old", "any", "same", "tell", "boy", "follow", "came",
        "want", "show", "also", "around", "form", "three", "small", "set", "put", "end",
        "does", "another", "well", "large", "must", "big", "even", "such", "because", "turn",
        "here", "why", "ask", "went", "men", "read", "need", "land", "different", "home",
        "us", "move", "try", "kind", "hand", "picture", "again", "change", "off", "play",
        "spell", "air", "away", "animal", "house", "point", "page", "letter", "mother", "answer",
        "found", "study", "still", "learn", "should", "America", "world", "high", "every", "near",
        "add", "food", "between", "own", "below", "country", "plant", "last", "school", "father",
        "keep", "tree", "never", "start", "city", "earth", "eye", "light", "thought", "head",
        "under", "story", "saw", "left", "don't", "few", "while", "along", "might", "close",
        "something", "seem", "next", "hard", "open", "example", "begin", "life", "always", "those",
        "both", "paper", "together", "got", "group", "often", "run", "important", "until", "children",
        "side", "feet", "car", "mile", "night", "walk", "white", "sea", "began", "grow",
        "took", "river", "four", "carry", "state", "once", "book", "hear", "stop", "without",
        "second", "later", "miss", "idea", "enough", "eat", "face", "watch", "far", "Indian",
        "really", "almost", "let", "above", "girl", "sometimes", "mountain", "cut", "young", "talk",
        "soon", "list", "song", "being", "leave", "family"
    ]

    # Check common words first
    for word in common_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hashes:
            idx = hashes.index(word_hash)
            decoded[idx] = word

    print(f"Found {len(decoded)} matches with common words.")

    # Try with a larger dictionary if available
    try:
        with open('/usr/share/dict/words', 'r') as dictionary:
            print("Checking with system dictionary...")
            for i, word in enumerate(dictionary):
                if i % 5000 == 0:
                    print(f"Progress: {i} words checked, found {len(decoded)} matches", end="\r")

                word = word.strip().lower()
                if len(word) > 1:  # Skip single characters
                    word_bytes = word.encode("utf-8")
                    word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                    if word_hash in hashes:
                        idx = hashes.index(word_hash)
                        if idx not in decoded:  # Only update if we didn't already decode this position
                            decoded[idx] = word
    except FileNotFoundError:
        print("System dictionary not found.")

    # Print results
    print(f"\nDecoded {len(decoded)}/{len(hashes)} words ({len(decoded)/len(hashes)*100:.1f}%)")

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded:
            message.append(decoded[i])
        else:
            message.append("[?]")

    # Print part of the message
    print("\nPartial decoded message:")
    print(" ".join(message[:50]) + "..." if len(message) > 50 else " ".join(message))

    # Save results to file
    with open(f"decoded_message_{key_str}.txt", "w") as f:
        f.write(f"Key: {key_str}\n")
        f.write(f"Decoded: {len(decoded)}/{len(hashes)} words ({len(decoded)/len(hashes)*100:.1f}%)\n\n")
        f.write("Message:\n")
        f.write(" ".join(message))
        f.write("\n\nDecoded positions:\n")
        for pos in sorted(decoded.keys()):
            f.write(f"{pos}: {decoded[pos]}\n")

    print(f"\nFull results saved to decoded_message_{key_str}.txt")

    return len(decoded)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_promising.py <key>")
        sys.exit(1)

    key = sys.argv[1]
    check_key(key)