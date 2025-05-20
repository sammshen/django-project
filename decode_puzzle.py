import hashlib
import sys

def decode_puzzle(key):
    # Read the puzzle file
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    print(f"Decoding PUZZLE with key: {key}")
    decoded_words = {}
    key_bytes = key.encode("utf-8")

    # Make a dict of hash -> index for easy lookup
    hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

    # Try to decode with a system dictionary if available
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
        print("System dictionary not found. Trying common words only.")

    # Try common words and words specific to the context
    context_words = [
        # Common English words
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',

        # Words from the known story context
        'agent', 'fly', 'from', 'mercy', 'superior', 'lake', 'three', 'oclock',
        'two', 'days', 'before', 'event', 'place', 'note', 'door', 'little',
        'yellow', 'house', 'wednesday', 'february', 'take', 'off', 'away',
        'own', 'wings', 'please', 'forgive', 'loved', 'robert', 'smith',
        'insurance', 'mutual', 'life', 'carolina', 'north', 'promised',
        'side', 'other', 'superior', 'tacked', 'signed', 'ins'
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
            message.append("[UNKNOWN:" + str(i) + "]")

    # Print stats
    decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))
    print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

    # Display the message
    print("\nDecoded message:")
    print(" ".join(message))

    # Save to file
    with open("decoded_message.txt", "w") as f:
        f.write(" ".join(message) + "\n\n")
        f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
        f.write("Remaining unknown indices:\n")
        for idx in range(len(hashes)):
            if idx not in decoded_words:
                f.write(f"{idx}: {hashes[idx]}\n")

    print(f"\nResults saved to decoded_message.txt")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        key = input("Enter the 9-digit key: ")

    decode_puzzle(key)