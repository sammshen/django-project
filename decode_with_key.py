import hashlib
import sys

def decode_puzzle(key):
    """Decode the puzzle with the given key."""
    # Read the puzzle file
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    print(f"Decoding puzzle with key: {key}")
    decoded_words = {}
    key_bytes = key.encode("utf-8")

    # Create a lookup dictionary
    hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

    # First, try with a comprehensive dictionary if available
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
        print("Dictionary file not found, using specific word lists only.")

    # Try context-specific words
    context_words = [
        # Common English words
        "the", "a", "an", "and", "of", "to", "in", "is", "you", "that", "it", "he",
        "was", "for", "on", "are", "as", "with", "his", "they", "I", "at", "be",
        "this", "have", "from", "or", "one", "had", "by", "but", "not", "what",
        "all", "were", "we", "when", "your", "can", "said", "there", "use",
        "each", "which", "she", "do", "how", "their", "if", "will", "up", "other",
        "about", "out", "many", "then", "them", "these", "so", "some", "her", "would",
        "make", "like", "him", "into", "time", "has", "look", "two", "more", "go",
        "see", "no", "way", "could", "my", "than", "been", "call", "who", "its",
        "now", "find", "long", "down", "day", "did", "get", "come", "made", "may",

        # Words known from the context
        "north", "carolina", "mutual", "life", "insurance", "agent", "promised",
        "fly", "from", "mercy", "to", "the", "other", "side", "of", "lake",
        "superior", "at", "three", "oclock", "o'clock", "clock", "two", "days",
        "before", "event", "place", "tacked", "note", "door", "little", "yellow",
        "house", "wednesday", "february", "take", "off", "away", "own",
        "wings", "please", "forgive", "me", "loved", "you", "all", "signed",
        "robert", "smith", "ins",

        # Variations
        "1931", "3:00", "p.m.", "18th", "pm", "am", "3", "00", "p", "m", "pm",
        "sincerely", "truly", "signature", "sign", "(signed)", "signed",
        "agent", "insurance", "insure", "mr", "mrs", "dr"
    ]

    for word in context_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        if word_hash in hash_to_index:
            idx = hash_to_index[word_hash]
            decoded_words[idx] = word

    # Reconstruct the message
    message = []
    for i in range(len(hashes)):
        if i in decoded_words:
            message.append(decoded_words[i])
        else:
            message.append(f"[{i}]")

    # Print stats
    decoded_count = sum(1 for word in message if not word.startswith("["))
    print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

    # Display the message
    print("\nDecoded message:")
    print(" ".join(message))

    # Save to file
    with open(f"decoded_message_{key}.txt", "w") as f:
        f.write(f"Key: {key}\n\n")
        f.write(" ".join(message) + "\n\n")
        f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
        f.write("Remaining unknown indices:\n")
        for i in range(len(hashes)):
            if i not in decoded_words:
                f.write(f"{i}: {hashes[i]}\n")

    print(f"\nResults saved to decoded_message_{key}.txt")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        key = input("Enter the 9-digit key: ")

    decode_puzzle(key)