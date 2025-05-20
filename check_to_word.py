import hashlib

def check_to_word():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the puzzle file to get the hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Calculate hash for the word "to"
    to_bytes = "to".encode("utf-8")
    to_hash = hashlib.md5(key_bytes + to_bytes).hexdigest()

    # Check where "to" occurs in the hash list
    to_positions = []
    for i, h in enumerate(hashes):
        if h == to_hash:
            to_positions.append(i)

    print(f"The hash for 'to' appears at positions: {to_positions}")

    # Expected text from the message
    text = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    # Get the words at these positions in the original text
    words = text.split()

    print("\nChecking which words in the original text were replaced by 'to':")
    for pos in to_positions:
        if pos < len(words):
            expected_word = words[pos].strip(".,!?;:'\"").lower()
            print(f"Position {pos}: Should be '{expected_word}' but hash matches 'to'")

            # Check if the expected word is similar to "to" (might be a typo)
            if "to" in expected_word or expected_word in "to":
                print(f"  - Note: '{expected_word}' contains or is contained in 'to'")

            # Check if removing a character makes it "to"
            for i in range(len(expected_word)):
                deleted = expected_word[:i] + expected_word[i+1:]
                if deleted == "to":
                    print(f"  - Note: Removing '{expected_word[i]}' from '{expected_word}' gives 'to'")

            # Check if adding a character makes it the expected word
            for i in range(len("to")+1):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    inserted = "to"[:i] + c + "to"[i:]
                    if inserted == expected_word:
                        print(f"  - Note: Adding '{c}' to 'to' gives '{expected_word}'")

    print("\nAnalyzing words similar to 'to':")
    for i, word in enumerate(words):
        clean_word = word.strip(".,!?;:'\"").lower()

        # Check if this word is similar to "to"
        if clean_word not in ["to"] and (len(clean_word) <= 4):
            # See if deleting a letter gives "to"
            for j in range(len(clean_word)):
                deleted = clean_word[:j] + clean_word[j+1:]
                if deleted == "to":
                    print(f"Word '{clean_word}' at position {i} becomes 'to' if '{clean_word[j]}' is deleted")

                    # Check if the hash for "to" matches the expected hash
                    if i < len(hashes):
                        expected_hash = hashes[i]
                        matches = "✓" if to_hash == expected_hash else "✗"
                        print(f"  - Hash for 'to' matches expected hash: {matches}")

if __name__ == "__main__":
    check_to_word()