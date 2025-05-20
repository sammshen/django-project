import hashlib
import itertools

# Read the puzzle file
with open("puzzle/PUZZLE-EASY", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# We know the key is 6346
key = "6346"
decoded_words = {}

# Create a hash -> index mapping
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# Function to check if a word matches any hash
def check_word(word):
    word_hash = hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
    if word_hash in hash_to_index:
        idx = hash_to_index[word_hash]
        if idx not in decoded_words:  # Don't overwrite existing decoded words
            decoded_words[idx] = word
            if word not in found_words:
                found_words.append(word)
                print(f"Found word: {word}")
            return True
    return False

# Our currently known partial message
partial_message = [None] * len(hashes)

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
for idx, word in known_words.items():
    partial_message[idx] = word

# Print what we currently know
print("Current partial message:")
print(" ".join([word if word else "[UNKNOWN]" for word in partial_message]))

# Track words we've found for reporting
found_words = []

# Names that might appear in the text
names = [
    "john", "james", "robert", "michael", "william", "david", "richard", "joseph",
    "thomas", "charles", "mary", "patricia", "jennifer", "elizabeth", "linda",
    "barbara", "susan", "margaret", "jessica", "sarah", "smith", "johnson", "brown",
    "jones", "miller", "davis", "wilson", "taylor", "clark", "hall", "lee"
]

# Locations that might appear in the text
locations = [
    "london", "paris", "berlin", "moscow", "rome", "vienna", "madrid", "prague",
    "amsterdam", "brussels", "washington", "york", "boston", "chicago", "los", "angeles",
    "san", "francisco", "austin", "dallas", "houston", "atlanta", "miami", "denver",
    "seattle", "portland", "philadelphia", "phoenix", "england", "france", "germany",
    "russia", "italy", "austria", "spain", "america", "europe", "asia", "america"
]

# Time-related words that might appear
time_words = [
    "morning", "afternoon", "evening", "night", "oclock", "am", "pm", "dawn", "dusk",
    "midnight", "noon", "today", "tomorrow", "yesterday", "monday", "tuesday",
    "wednesday", "thursday", "friday", "saturday", "sunday", "january", "february",
    "march", "april", "may", "june", "july", "august", "september", "october",
    "november", "december", "week", "month", "year", "day", "hour", "minute", "second"
]

# Buildings or structures
buildings = [
    "house", "home", "apartment", "flat", "condo", "cabin", "cottage", "mansion",
    "palace", "castle", "hotel", "motel", "inn", "hostel", "building", "tower",
    "skyscraper", "office", "headquarters", "base", "station", "airport", "terminal",
    "hangar", "garage", "barn", "shed", "hut", "shack", "bunker", "shelter", "post"
]

# Transportation related
transportation = [
    "airplane", "plane", "jet", "helicopter", "chopper", "aircraft", "fighter",
    "bomber", "car", "truck", "van", "suv", "vehicle", "automobile", "motorcycle",
    "bike", "bicycle", "boat", "ship", "yacht", "submarine", "train", "subway", "tram",
    "bus", "taxi", "cab", "limo", "limousine", "coach", "carriage", "sled", "sleigh"
]

# Communication related
communication = [
    "message", "letter", "note", "email", "text", "call", "phone", "telegram",
    "radio", "broadcast", "signal", "code", "cipher", "password", "word", "sign",
    "symbol", "signal", "message", "mail", "post", "postcard", "envelope", "package"
]

# Espionage related
espionage = [
    "agent", "spy", "operative", "officer", "intelligence", "counter", "mission",
    "operation", "assignment", "task", "duty", "job", "cover", "handler", "asset",
    "informant", "mole", "double", "triple", "secret", "classified", "confidential",
    "restricted", "clearance", "authorization", "badge", "id", "identification",
    "agency", "bureau", "division", "department", "branch", "cell", "network", "ring",
    "group", "team", "unit", "squad", "force", "command", "headquarters", "base",
    "station", "post", "outpost", "safe", "house", "meeting", "rendezvous", "drop",
    "pickup", "extraction", "escape", "evasion", "surveillance", "observation",
    "recon", "reconnaissance", "intelligence", "information", "data", "file", "dossier",
    "report", "briefing", "debriefing", "communication", "transmission", "intercept",
    "decrypt", "encrypt", "code", "cipher", "password", "passphrase", "credentials",
    "security", "breach", "compromise", "defect", "defector", "traitor", "double", "agent"
]

# Colors that might be relevant (given "yellow" is in the text)
colors = [
    "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black",
    "white", "gray", "grey", "gold", "silver", "bronze", "copper", "ivory", "cream"
]

# Additional relevant words based on what we've decoded
additional_words = [
    # Beginnings of message
    "this", "dear", "attention", "urgent", "warning", "notice", "alert", "important",
    "confidential", "classified", "secret", "top", "for", "regarding", "re", "subject",
    "concerning", "about", "briefing", "debriefing", "report", "update", "status",

    # Specific to our message context
    "shall", "must", "need", "going", "planning", "decided", "chosen", "elected",
    "agreed", "determined", "resolved", "committed", "dedicated", "devoted", "sworn",
    "pledged", "vowed", "promised", "intended", "meant", "purposed", "designed",
    "aimed", "targeted", "destined", "fated", "doomed", "condemned", "sentenced",
    "ordered", "commanded", "directed", "instructed", "told", "advised", "suggested",
    "recommended", "urged", "encouraged", "persuaded", "convinced", "compelled",
    "forced", "obligated", "obliged", "required", "mandated", "assigned", "appointed",
    "designated", "selected", "picked", "chosen", "named", "called", "labeled",
    "tagged", "marked", "branded", "stamped", "sealed", "certified", "approved",
    "authorized", "permitted", "allowed", "sanctioned", "granted", "issued", "given",
    "blessed", "cursed", "damned", "condemned",

    # Words related to writing a note
    "wrote", "written", "penned", "scribbled", "jotted", "drafted", "composed",
    "inscribed", "left", "posted", "pinned", "taped", "stuck", "attached", "affixed",
    "fastened", "secured", "placed", "put", "set", "laid", "rested", "deposited",
    "situated", "stationed", "positioned", "arranged", "settled", "established",
    "fixed", "installed", "mounted", "hung", "displayed", "exhibited", "shown",
    "presented", "offered", "proposed", "suggested", "recommended", "advised",

    # Words to fill in blanks
    "please", "kindly", "humbly", "sincerely", "truly", "honestly", "frankly",
    "openly", "directly", "plainly", "simply", "clearly", "definitely", "certainly",
    "surely", "undoubtedly", "unquestionably", "indisputably", "inarguably",
    "incontestably", "incontrovertibly", "irrefutably", "indubitably", "absolutely",
    "positively", "completely", "entirely", "totally", "wholly", "fully", "perfectly",
    "exactly", "precisely", "accurately", "correctly", "properly", "appropriately",
    "suitably", "fittingly", "aptly", "relevantly", "pertinently", "accordingly",
    "correspondingly", "consistently", "congruously", "harmoniously", "compatibly"
]

# Common verbs that might fill in the blanks
common_verbs = [
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
    "do", "does", "did", "done", "doing", "go", "goes", "went", "gone", "going",
    "come", "comes", "came", "coming", "see", "sees", "saw", "seen", "seeing",
    "know", "knows", "knew", "known", "knowing", "get", "gets", "got", "gotten",
    "getting", "make", "makes", "made", "making", "say", "says", "said", "saying",
    "think", "thinks", "thought", "thinking", "take", "takes", "took", "taken",
    "taking", "find", "finds", "found", "finding", "give", "gives", "gave", "given",
    "giving", "tell", "tells", "told", "telling", "work", "works", "worked", "working",
    "call", "calls", "called", "calling", "try", "tries", "tried", "trying", "ask",
    "asks", "asked", "asking", "need", "needs", "needed", "needing", "feel", "feels",
    "felt", "feeling", "become", "becomes", "became", "becoming", "leave", "leaves",
    "left", "leaving", "put", "puts", "putting", "mean", "means", "meant", "meaning",
    "keep", "keeps", "kept", "keeping", "let", "lets", "letting", "begin", "begins",
    "began", "begun", "beginning", "seem", "seems", "seemed", "seeming", "help",
    "helps", "helped", "helping", "talk", "talks", "talked", "talking", "turn",
    "turns", "turned", "turning", "start", "starts", "started", "starting", "show",
    "shows", "showed", "shown", "showing", "hear", "hears", "heard", "hearing", "play",
    "plays", "played", "playing", "run", "runs", "ran", "running", "move", "moves",
    "moved", "moving", "live", "lives", "lived", "living", "believe", "believes",
    "believed", "believing", "bring", "brings", "brought", "bringing", "happen",
    "happens", "happened", "happening", "write", "writes", "wrote", "written",
    "writing", "sit", "sits", "sat", "sitting", "stand", "stands", "stood", "standing",
    "lose", "loses", "lost", "losing", "pay", "pays", "paid", "paying", "meet",
    "meets", "met", "meeting", "include", "includes", "included", "including", "continue",
    "continues", "continued", "continuing", "set", "sets", "setting", "learn", "learns",
    "learned", "learning", "change", "changes", "changed", "changing", "lead", "leads",
    "led", "leading", "understand", "understands", "understood", "understanding", "watch",
    "watches", "watched", "watching", "follow", "follows", "followed", "following"
]

# Common prepositions that might fill in the blanks
common_prepositions = [
    "about", "above", "across", "after", "against", "along", "amid", "among",
    "around", "as", "at", "before", "behind", "below", "beneath", "beside",
    "between", "beyond", "but", "by", "concerning", "considering", "despite",
    "down", "during", "except", "for", "from", "in", "inside", "into", "like",
    "near", "of", "off", "on", "onto", "out", "outside", "over", "past", "regarding",
    "round", "since", "through", "throughout", "till", "to", "toward", "towards",
    "under", "underneath", "until", "unto", "up", "upon", "with", "within", "without"
]

# Combine all our word lists
all_words = []
all_words.extend(names)
all_words.extend(locations)
all_words.extend(time_words)
all_words.extend(buildings)
all_words.extend(transportation)
all_words.extend(communication)
all_words.extend(espionage)
all_words.extend(colors)
all_words.extend(additional_words)
all_words.extend(common_verbs)
all_words.extend(common_prepositions)

# Remove duplicates
all_words = list(set(all_words))
print(f"Trying {len(all_words)} words...")

# Try each word
for word in all_words:
    word = word.strip().lower()
    if word:
        check_word(word)

# Specific phrases for specific positions
# Based on context and our knowledge of the story so far
print("\nTrying specific words based on the context...")

# Try specific words for specific positions
specific_positions = {
    # Based on context: "agent promised to fly from [PLACE] to the other side of [PLACE]"
    11: ["london", "paris", "berlin", "moscow", "america", "europe", "russia", "york",
         "washington", "langley", "headquarters", "here", "home", "base", "station",
         "country", "homeland"],

    # Based on context: "to the other side of [LOCATION/DESCRIPTION] [LOCATION/DESCRIPTION]"
    17: ["the", "this", "our", "their", "that", "his", "her", "its", "your",
         "these", "those", "some", "any", "no", "all", "each", "either", "neither",
         "both", "such", "what", "which", "whose", "who", "whom", "where", "when",
         "why", "how", "many", "much", "few", "little", "several", "enough", "plenty",
         "cold", "frozen", "icy", "warm", "hot", "burning", "flaming", "bright", "dark",
         "sunny", "cloudy", "rainy", "snowy", "foggy", "misty", "stormy", "calm",
         "peaceful", "quiet", "silent", "noisy", "loud", "dangerous", "safe", "secure"],

    18: ["world", "country", "ocean", "sea", "mountain", "river", "lake", "forest",
         "city", "town", "village", "border", "frontier", "curtain", "wall", "fence",
         "line", "divide", "boundary", "territory", "realm", "domain", "land", "earth",
         "globe", "planet", "continent", "subcontinent", "region", "area", "zone",
         "sector", "district", "province", "state", "county", "parish", "township"],

    # Based on context: "at three [TIME] [TIME] days before"
    21: ["am", "pm", "oclock", "hours", "hundred", "thirty", "forty", "fifty",
         "minutes", "seconds", "in", "sharp", "precisely", "exactly", "approximately",
         "about", "around", "nearly", "almost", "just", "barely", "hardly", "scarcely"],

    22: ["pm", "am", "oclock", "hundred", "thirty", "minutes", "seconds", "hours",
         "in", "on", "at", "the", "of", "by", "until", "till", "before", "after",
         "during", "throughout", "within", "between", "among", "amid", "amidst",
         "morning", "afternoon", "evening", "night", "midnight", "noon", "dawn", "dusk"],

    # Based on context: "little yellow [OBJECT]"
    42: ["house", "home", "cottage", "cabin", "building", "car", "truck", "van",
         "vehicle", "airplane", "plane", "jet", "helicopter", "boat", "ship", "yacht",
         "submarine", "notebook", "notepad", "pad", "paper", "envelope", "card",
         "postcard", "letter", "message", "sign", "signal", "flag", "banner", "emblem",
         "symbol", "umbrella", "parasol", "sunshade", "hat", "cap", "helmet", "mask",
         "glasses", "spectacles", "goggles", "binoculars", "telescope", "microscope",
         "camera", "box", "case", "container", "jar", "bottle", "flask", "vial",
         "tube", "pipe", "wire", "cable", "cord", "rope", "string", "thread", "line",
         "aircraft", "helicopter", "plane", "airplane", "jet", "glider"],

    # Words that might follow "little yellow [OBJECT] [???]"
    43: ["with", "that", "which", "where", "when", "while", "whilst", "whereas",
         "whereupon", "wherefore", "whereafter", "whereat", "whereby", "wherein",
         "whereof", "whereon", "wheresoever", "whereunto", "wherewith", "wherever",
         "and", "but", "or", "nor", "for", "so", "yet", "as", "if", "though", "although",
         "even", "because", "since", "unless", "until", "while", "where", "when", "after"],

    # Based on context around the text
    65: ["please", "kindly", "just", "do", "but", "and", "you", "all", "everyone",
         "anybody", "somebody", "nobody", "everybody", "anyone", "someone", "no one",
         "everyone", "now", "then", "here", "there", "soon", "later", "today", "tomorrow",
         "tonight", "this", "that", "these", "those", "such", "which", "what", "whose",
         "who", "whom", "where", "when", "why", "how", "whither", "whence", "whereby",
         "wherefore", "whereafter", "whereas", "whereupon", "wherewith", "wherever"],
}

# Try custom words for specific positions
for position, word_list in specific_positions.items():
    print(f"Trying specific words for position {position}...")
    for word in word_list:
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

# Print remaining unknown hashes
if decoded_count < len(hashes):
    print("\nRemaining unknown hash indexes:")
    unknown_indexes = [i for i in range(len(hashes)) if i not in decoded_words]
    for idx in unknown_indexes:
        print(f"{idx}: {hashes[idx]}")

# Write results to file
with open("decoded_easy_message.txt", "w") as f:
    f.write(" ".join(message) + "\n\n")
    f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
    f.write("Key: " + key + "\n\n")
    f.write("Remaining unknown hashes:\n")
    for i in range(len(hashes)):
        if i not in decoded_words:
            f.write(f"{i}: {hashes[i]}\n")