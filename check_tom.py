import hashlib

def check_tom():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    hash_set = set(hashes)

    # Variations of "Tom" to check
    variations = ["Tom", "tom", "To", "to", "om", "Tm", "tm", "TOm", "tOm", "toM"]

    print("Checking variations of 'Tom':")
    for var in variations:
        var_bytes = var.encode("utf-8")
        var_hash = hashlib.md5(key_bytes + var_bytes).hexdigest()

        if var_hash in hash_set:
            pos = hashes.index(var_hash)
            print(f"Found: '{var}' at position {pos}")
            print(f"Hash: {var_hash}")

    # Look for position 140 which should have "Tom," from the message
    expected_position = 140
    if expected_position < len(hashes):
        expected_hash = hashes[expected_position]
        print(f"\nHash at position {expected_position}: {expected_hash}")

        # Try many variants to find what word matches this hash
        all_possible = []

        # Add common characters to create variations
        for c in "abcdefghijklmnopqrstuvwxyz":
            all_possible.append("t" + c)
            all_possible.append("t" + c + "m")
            all_possible.append("to" + c)
            all_possible.append(c + "om")
            all_possible.append(c + "o")
            all_possible.append("t" + c)

        # Add variations like "t0m" (with numbers)
        for n in "0123456789":
            all_possible.append("t" + n + "m")
            all_possible.append("t" + n)
            all_possible.append("t" + "o" + n)

        # Add common variations of "Tom" and other similar words
        all_possible.extend([
            "tom", "Tom", "TOM", "to", "To", "TO", "toom", "tommm", "tooom",
            "tommy", "thomas", "tolm", "totm", "torm", "tonm", "toml", "tomm"
        ])

        # Check all these variations
        print(f"Checking {len(all_possible)} possible variations for position {expected_position}...")
        for var in all_possible:
            var_bytes = var.encode("utf-8")
            var_hash = hashlib.md5(key_bytes + var_bytes).hexdigest()

            if var_hash == expected_hash:
                print(f"Match found! '{var}' generates hash {expected_hash}")

if __name__ == "__main__":
    check_tom()