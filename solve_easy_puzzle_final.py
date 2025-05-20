import hashlib
import string

# Read the puzzle file
with open("puzzle/PUZZLE-EASY", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# We know the key is 6346
key = "6346"
decoded_words = {}

# Create a hash -> index mapping
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# Patterns we observe in the partially decoded message
# [UNKNOWN] [UNKNOWN] [UNKNOWN] [UNKNOWN] [UNKNOWN] [UNKNOWN] agent promised to fly from [UNKNOWN] to
# the other side of [UNKNOWN] [UNKNOWN] at three [UNKNOWN] [UNKNOWN] days before the event was to take
# place he tacked a note on the door of his little yellow [UNKNOWN] [UNKNOWN] [UNKNOWN] [UNKNOWN] on
# [UNKNOWN] the [UNKNOWN] of [UNKNOWN] [UNKNOWN] [UNKNOWN] will take off from [UNKNOWN] and fly away
# on my own [UNKNOWN] [UNKNOWN] forgive [UNKNOWN] [UNKNOWN] I loved you [UNKNOWN] [UNKNOWN] [UNKNOWN]
# [UNKNOWN] [UNKNOWN] agent

# Function to check if a word matches any hash
def check_word(word):
    word_hash = hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
    if word_hash in hash_to_index:
        idx = hash_to_index[word_hash]
        if idx not in decoded_words:  # Don't overwrite existing decoded words
            decoded_words[idx] = word
            print(f"Found new word at position {idx}: {word}")
            return True
    return False

# Words we've already decoded
known_words = {
    6: "agent",
    7: "promised",
    8: "to",
    9: "fly",
    10: "from",
    12: "to",
    13: "the",
    14: "other",
    15: "side",
    16: "of",
    19: "at",
    20: "three",
    23: "days",
    24: "before",
    25: "the",
    26: "event",
    27: "was",
    28: "to",
    29: "take",
    30: "place",
    31: "he",
    32: "tacked",
    33: "a",
    34: "note",
    35: "on",
    36: "the",
    37: "door",
    38: "of",
    39: "his",
    40: "little",
    41: "yellow",
    46: "on",
    48: "the",
    50: "of",
    54: "will",
    55: "take",
    56: "off",
    57: "from",
    59: "and",
    60: "fly",
    61: "away",
    62: "on",
    63: "my",
    64: "own",
    67: "forgive",
    70: "I",
    71: "loved",
    72: "you",
    77: "agent"
}

# Update our decoded words from what we know
decoded_words.update(known_words)

# Now let's try to complete the specific sentences and common patterns
beginnings = [
    "the", "a", "an", "this", "that", "these", "those", "my", "our", "your", "his", "her", "their",
    "dear", "to", "from", "for", "in", "with", "by", "at", "on", "top", "confidential", "secret",
    "urgent", "important", "attention", "notice", "warning", "alert", "message", "memo", "letter",
    "official", "classified", "restricted"
]

# Try beginnings of the message (positions 0-5)
print("\nTrying possible beginnings for positions 0-5...")
for pos in range(6):
    for word in beginnings:
        check_word(word)

# For position 11 (after "fly from"): likely a location
locations = [
    "home", "base", "here", "headquarters", "office", "station", "post", "duty", "assignment",
    "position", "location", "america", "europe", "asia", "africa", "australia", "antarctica",
    "north", "south", "east", "west", "central", "washington", "london", "paris", "berlin",
    "moscow", "rome", "madrid", "vienna", "prague", "tokyo", "beijing", "delhi", "cairo",
    "york", "chicago", "los", "angeles", "francisco", "boston", "seattle", "atlanta", "miami",
    "dallas", "houston", "denver", "phoenix", "philadelphia", "detroit", "cleveland", "portland",
    "country", "state", "city", "town", "village", "province", "territory", "region", "area",
    "zone", "sector", "district", "neighborhood", "street", "avenue", "boulevard", "road",
    "highway", "route", "path", "trail", "way", "lane", "drive", "place", "court", "plaza",
    "square", "circle", "park", "garden", "forest", "jungle", "desert", "mountain", "valley",
    "hill", "cliff", "canyon", "gorge", "ravine", "gulch", "pass", "ridge", "peak", "summit",
    "plateau", "mesa", "plain", "prairie", "steppe", "tundra", "marsh", "swamp", "bog", "fen",
    "moor", "lagoon", "lake", "sea", "ocean", "bay", "gulf", "strait", "channel", "sound",
    "river", "stream", "creek", "brook", "spring", "waterfall", "cascade", "rapids", "dam"
]

# Position 11 (after "fly from")
print("\nTrying possible locations for position 11...")
for word in locations:
    check_word(word)

# For positions 17-18 (after "other side of")
descriptions = [
    "the", "this", "that", "these", "those", "our", "your", "his", "her", "their", "its",
    "iron", "steel", "metal", "wooden", "concrete", "stone", "brick", "glass", "plastic",
    "cold", "frozen", "hot", "burning", "dark", "bright", "sunny", "cloudy", "rainy", "foggy",
    "snowy", "stormy", "windy", "calm", "peaceful", "quiet", "loud", "noisy", "dangerous",
    "safe", "secure", "protected", "guarded", "watched", "monitored", "observed", "seen",
    "hidden", "concealed", "covered", "exposed", "open", "closed", "locked", "unlocked",
    "barred", "gated", "fenced", "walled", "bordered", "bounded", "limited", "restricted",
    "controlled", "regulated", "governed", "ruled", "managed", "administered", "supervised"
]

locations_and_boundaries = [
    "world", "country", "nation", "state", "border", "frontier", "boundary", "line", "divide",
    "curtain", "wall", "fence", "barrier", "ocean", "sea", "river", "mountain", "range",
    "territory", "city", "town", "village", "district", "region", "zone", "sector", "area",
    "space", "room", "field", "park", "forest", "desert", "island", "peninsula", "continent",
    "hemisphere", "globe", "earth", "land", "water", "air", "sky", "space", "universe", "realm",
    "domain", "kingdom", "empire", "republic", "federation", "union", "alliance", "coalition",
    "bloc", "camp", "side", "team", "group", "clan", "tribe", "nation", "people", "culture",
    "civilization", "society", "community", "neighborhood", "district", "ward", "precinct"
]

# Positions 17-18 (after "other side of")
print("\nTrying possible descriptions for position 17...")
for word in descriptions:
    check_word(word)

print("\nTrying possible locations/boundaries for position 18...")
for word in locations_and_boundaries:
    check_word(word)

# For positions 21-22 (after "at three")
time_words = [
    "am", "pm", "o'clock", "oclock", "hours", "minutes", "seconds", "in", "the", "morning",
    "afternoon", "evening", "night", "dawn", "dusk", "midnight", "noon", "midday", "days",
    "weeks", "months", "years", "decades", "centuries", "millennia", "eras", "ages", "periods",
    "times", "moments", "instances", "occasions", "events", "happenings", "occurrences", "sharp",
    "exactly", "precisely", "approximately", "about", "around", "nearly", "almost", "just", "barely"
]

# Positions 21-22 (after "at three")
print("\nTrying possible time words for positions 21-22...")
for word in time_words:
    check_word(word)

# For position 42 (after "little yellow")
objects = [
    "house", "home", "cottage", "cabin", "shack", "hut", "apartment", "flat", "condo", "room",
    "car", "truck", "van", "suv", "vehicle", "automobile", "motorcycle", "bike", "bicycle",
    "airplane", "plane", "jet", "helicopter", "aircraft", "boat", "ship", "yacht", "submarine",
    "train", "bus", "taxi", "cab", "limo", "notebook", "notepad", "pad", "paper", "envelope",
    "card", "postcard", "letter", "message", "sign", "signal", "flag", "banner", "emblem",
    "symbol", "book", "journal", "diary", "log", "ledger", "record", "document", "file", "folder",
    "box", "case", "container", "jar", "bottle", "flask", "vial", "tube", "pipe", "wire", "cable",
    "cord", "rope", "string", "thread", "line", "suit", "outfit", "costume", "uniform", "dress",
    "shirt", "pants", "trousers", "shorts", "skirt", "jacket", "coat", "sweater", "sweatshirt",
    "hoodie", "hat", "cap", "helmet", "mask", "glasses", "goggles", "umbrella", "parasol", "fan",
    "handbag", "purse", "wallet", "backpack", "bag", "sack", "pack", "bundle", "bird", "dog", "cat"
]

# Position 42 (after "little yellow")
print("\nTrying possible objects for position 42...")
for word in objects:
    check_word(word)

# For positions 43-47 (structure after "yellow [OBJECT]")
structure_words = [
    "and", "with", "that", "which", "where", "while", "as", "like", "so", "but", "or", "nor",
    "yet", "for", "therefore", "thus", "hence", "consequently", "accordingly", "because",
    "since", "if", "unless", "until", "though", "although", "even", "read", "said", "stated",
    "wrote", "declared", "proclaimed", "announced", "revealed", "disclosed", "divulged",
    "confessed", "admitted", "acknowledged", "conceded", "granted", "allowed", "permitted"
]

# Positions 43-47 (structure after "yellow [OBJECT]")
print("\nTrying possible structure words for positions 43-47...")
for word in structure_words:
    check_word(word)

# For position 58 (second "from" location, same as position 11)
print("\nTrying possible locations for position 58 (same as position 11)...")
for word in locations:
    check_word(word)

# For positions 65-69 (around "forgive")
final_plea = [
    "please", "do", "just", "must", "should", "can", "may", "might", "could", "would", "will",
    "shall", "try", "to", "and", "but", "or", "if", "then", "now", "soon", "later", "today",
    "tomorrow", "forever", "always", "never", "again", "once", "twice", "thrice", "too", "also",
    "as", "well", "such", "so", "very", "truly", "really", "actually", "indeed", "certainly",
    "definitely", "absolutely", "completely", "entirely", "totally", "wholly", "fully", "greatly",
    "greatly", "sincerely", "honestly", "truly", "faithfully", "loyally", "devotedly", "all",
    "me", "my", "mine", "myself", "you", "your", "yours", "yourself", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "we", "us", "our", "ours", "ourselves",
    "they", "them", "their", "theirs", "themselves", "anyone", "everyone", "someone", "no one",
    "anybody", "everybody", "somebody", "nobody", "anything", "everything", "something", "nothing",
    "for", "what", "i've", "done", "said", "meant", "intended", "thought", "planned", "decided",
    "chosen", "picked", "selected", "determined", "resolved", "committed", "dedicated", "devoted"
]

# For positions 65-69 (around "forgive")
print("\nTrying possible words for final plea (positions 65-69)...")
for word in final_plea:
    check_word(word)

# For positions 73-76 (final words before "agent")
final_words = [
    "your", "loyal", "faithful", "devoted", "dedicated", "committed", "trusted", "valued",
    "esteemed", "respected", "admired", "revered", "honored", "noble", "brave", "courageous",
    "valiant", "heroic", "fearless", "intrepid", "bold", "daring", "audacious", "adventurous",
    "former", "ex", "previous", "past", "old", "longtime", "veteran", "experienced", "seasoned",
    "trained", "skilled", "qualified", "competent", "capable", "able", "proficient", "expert",
    "master", "top", "chief", "head", "lead", "senior", "junior", "assistant", "deputy", "associate",
    "humble", "obedient", "subservient", "compliant", "submissive", "yielding", "acquiescent",
    "amenable", "tractable", "docile", "manageable", "controllable", "governable", "trainable",
    "foreign", "domestic", "international", "national", "local", "regional", "global", "worldwide",
    "universal", "federal", "state", "provincial", "territorial", "colonial", "imperial", "royal",
    "regal", "sovereign", "supreme", "paramount", "preeminent", "foremost", "first", "primary",
    "principal", "main", "major", "dominant", "predominant", "prevailing", "ruling", "reigning",
    "governing", "controlling", "commanding", "leading", "guiding", "directing", "managing",
    "friend", "ally", "partner", "colleague", "associate", "companion", "comrade", "fellow",
    "brother", "sister", "father", "mother", "son", "daughter", "child", "parent", "spouse",
    "husband", "wife", "fiancé", "fiancée", "boyfriend", "girlfriend", "lover", "sweetheart",
    "darling", "dear", "beloved", "precious", "cherished", "treasured", "adored", "worshipped",
    "idolized", "deified", "exalted", "glorified", "hallowed", "sanctified", "consecrated",
    "blessed", "sacred", "holy", "divine", "heavenly", "celestial", "ethereal", "spiritual",
    "good", "better", "best", "fine", "great", "excellent", "superb", "outstanding", "exceptional",
    "extraordinary", "remarkable", "phenomenal", "magnificent", "marvelous", "wonderful",
    "fantastic", "fabulous", "terrific", "tremendous", "stupendous", "incredible", "amazing",
    "astonishing", "astounding", "surprising", "shocking", "startling", "staggering", "stunning",
    "breathtaking", "awe-inspiring", "impressive", "imposing", "striking", "dramatic", "sensational"
]

# For positions 73-76 (final words before "agent")
print("\nTrying possible final words (positions 73-76)...")
for word in final_words:
    check_word(word)

# For hash values that appear multiple times, make sure they map to the same word
print("\nChecking for repeated hashes...")
hash_to_word = {}
for idx, word in decoded_words.items():
    hash_value = hashes[idx]
    hash_to_word[hash_value] = word

# Ensure consistency across repeated hashes
for idx, hash_val in enumerate(hashes):
    if hash_val in hash_to_word and idx not in decoded_words:
        decoded_words[idx] = hash_to_word[hash_val]
        print(f"Applied word '{hash_to_word[hash_val]}' to position {idx} based on hash match")

# Reconstruct the message
message = []
for i in range(len(hashes)):
    if i in decoded_words:
        message.append(decoded_words[i])
    else:
        message.append(f"[UNKNOWN-{i}:{hashes[i][:8]}]")

print("\nDecoded message:")
print(" ".join(message))

# Print stats
decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))
print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

# Analyze the remaining unknown words
if decoded_count < len(hashes):
    print("\nRemaining unknown hash indexes:")
    unknown_indexes = [i for i in range(len(hashes)) if i not in decoded_words]
    for idx in unknown_indexes:
        print(f"{idx}: {hashes[idx]}")

# Extract all known words to help with future decoding
print("\nAll decoded words:")
all_known_words = set(decoded_words.values())
for word in sorted(all_known_words):
    print(word)

# Write results to file
with open("decoded_easy_message.txt", "w") as f:
    f.write(" ".join(message) + "\n\n")
    f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
    f.write("Key: " + key + "\n\n")
    f.write("All decoded words:\n")
    for word in sorted(all_known_words):
        f.write(word + "\n")
    f.write("\nRemaining unknown hashes:\n")
    for i in range(len(hashes)):
        if i not in decoded_words:
            f.write(f"{i}: {hashes[i]}\n")