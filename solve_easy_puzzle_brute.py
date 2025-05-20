import hashlib
import time
import string
import itertools

# Read the puzzle file
with open("puzzle/PUZZLE-EASY", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# We know the key is 6346
key = "6346"

# Create a hash -> index mapping
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# We have already decoded these words
decoded_words = {
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

# Current hash values we need to decode
target_hashes = [
    (0, "990ccc807ea4c40834cc72860e9ab44d"),
    (1, "e642d9bb0039777f1c9450ae0f71d8f8"),
    (2, "a2dd34c85941dd5fbf0f5d819213bce7"),
    (3, "74e6f00a5ebe5893a156c4fefbdb9015"),
    (4, "b65fa5ebc290935b8a898e8e18f8f3b9"),
    (5, "2b2dc19fdc3420e795f268c4b18e4b84"),
    (11, "191da8afa63172d2a2f83a107e7a6269"),
    (17, "f8e8025855bcf5b049fa2a7b38bbc2cd"),
    (18, "838c88fafcef3b9a4d51b16ad54598df"),
    (21, "1f4c9b32e77767c8309bc1d9917033de"),
    (22, "cd7d93a475ac25092995d53af560eacb"),
    (42, "f8f010db1a5417d0b1ca413dcfe289a6"),
    (43, "7fe63627ed8d0bb5af782c9bd642bfcc"),
    (44, "99eb171291b15c04dc5385ee98d20ae7"),
    (45, "40dccde946c28c6bcd17edc5c903b599"),
    (47, "66dec4c8d7559e64580daf9f514400a1"),
    (49, "b848f0953aa35c7404f5c8735d3af6a3"),
    (51, "cdfcd8b17ef8c8275cf8078f86a9cdab"),
    (52, "7bdcc89c273dab6d0525d7642857881d"),
    (53, "3e9eaacc9699c81a2c58c2bf604a7471"),
    (58, "191da8afa63172d2a2f83a107e7a6269"),
    (65, "65a81a11492b05a13f8a306989e180ed"),
    (66, "2db0642807b5ecbb3052dd1c048db87a"),
    (68, "375795482194d747fcb0af4a69543c43"),
    (69, "3e9eaacc9699c81a2c58c2bf604a7471"),
    (73, "68ff83974f9ac73d9b748fe24747cd5a"),
    (74, "28b1c96dc3e5e714c769a02e1cf770a2"),
    (75, "f3b450d6788a4f2708a763656aeebe22"),
    (76, "1e72e518ccf2ad858bb4664fd97d1b9f")
]

# Dictionary to store any new words we find
new_words = {}

# Generate hash for a word
def get_hash(word):
    return hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()

# Check if a word matches any of our target hashes
def check_word(word):
    word_hash = get_hash(word)
    for pos, hash_val in target_hashes:
        if word_hash == hash_val:
            new_words[pos] = word
            print(f"Found word at position {pos}: '{word}'")
            return True
    return False

# Create very specific word lists for each position based on context

# For the beginning of the message (positions 0-5)
# [?] [?] [?] [?] [?] [?] agent promised to fly...
beginning_words = [
    "top", "secret", "confidential", "classified", "restricted", "urgent", "priority",
    "immediate", "important", "critical", "vital", "essential", "necessary", "required",
    "official", "formal", "informal", "personal", "private", "public", "internal", "external",
    "open", "closed", "limited", "unlimited", "special", "general", "standard", "exceptional",
    "emergency", "security", "clearance", "level", "tier", "grade", "class", "category",
    "code", "designation", "status", "condition", "situation", "circumstance", "position",
    "location", "destination", "origin", "source", "target", "objective", "goal", "aim",
    "purpose", "intention", "directive", "order", "command", "instruction", "guidance",
    "briefing", "debriefing", "report", "message", "communication", "transmission",
    "this", "that", "these", "those", "here", "there", "now", "then", "soon", "later",
    "today", "tomorrow", "yesterday", "morning", "afternoon", "evening", "night",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "dear", "to", "from", "for",
    "attention", "re", "subject", "regarding", "concerning", "about", "notice", "warning",
    "alert", "update", "reminder", "notification", "advisory", "bulletin", "memorandum",
    "communique", "dispatch", "directive", "protocol", "procedure", "regulation", "rule",
    "policy", "guideline", "standard", "specification", "requirement", "mandate", "dictate",
    "edict", "decree", "pronouncement", "declaration", "proclamation", "statement", "announcement"
]

# For position 11 (from [?] to the other side...)
# A location after "fly from"
locations = [
    "here", "there", "home", "base", "headquarters", "office", "station", "post", "duty",
    "america", "europe", "asia", "africa", "australia", "russia", "china", "india", "japan",
    "germany", "france", "england", "italy", "spain", "canada", "mexico", "brazil", "argentina",
    "washington", "london", "paris", "berlin", "moscow", "rome", "madrid", "tokyo", "beijing",
    "delhi", "cairo", "sydney", "toronto", "mexico", "brasilia", "buenos", "aires", "new",
    "york", "los", "angeles", "chicago", "houston", "philadelphia", "phoenix", "san", "diego",
    "dallas", "san", "jose", "austin", "jacksonville", "fort", "worth", "columbus", "charlotte",
    "indianapolis", "san", "francisco", "seattle", "denver", "boston", "el", "paso", "detroit",
    "nashville", "portland", "oklahoma", "las", "vegas", "memphis", "louisville", "baltimore",
    "milwaukee", "albuquerque", "tucson", "fresno", "sacramento", "kansas", "mesa", "atlanta",
    "omaha", "colorado", "raleigh", "miami", "oakland", "minneapolis", "tulsa", "cleveland",
    "wichita", "arlington", "new", "orleans", "bakersfield", "tampa", "aurora", "honolulu",
    "anaheim", "santa", "ana", "corpus", "christi", "riverside", "lexington", "st", "louis",
    "stockton", "pittsburgh", "saint", "paul", "cincinnati", "anchorage", "henderson", "greensboro",
    "plano", "newark", "lincoln", "toledo", "orlando", "chula", "vista", "irvine", "fort",
    "wayne", "jersey", "durham", "madison", "lubbock", "gilbert", "winston", "salem", "glendale",
    "huntington", "beach", "reno", "paradise", "chesapeake", "north", "vegas", "norfolk", "irving",
    "virginia", "beach", "city", "town", "village", "settlement", "community", "neighborhood",
    "district", "borough", "township", "municipality", "county", "parish", "province", "state",
    "territory", "region", "area", "zone", "sector", "district", "precinct", "ward", "quarter",
    "development", "complex", "compound", "installation", "facility", "establishment", "institute",
    "institution", "center", "building", "structure", "construction", "development", "project",
    "site", "location", "position", "place", "spot", "point", "area", "region", "zone", "sector",
    "territory", "realm", "domain", "kingdom", "empire", "republic", "nation", "country", "land",
    "continent", "island", "peninsula", "coast", "shore", "beach", "bay", "gulf", "strait",
    "channel", "sound", "sea", "ocean", "lake", "pond", "river", "stream", "brook", "creek",
    "mountain", "hill", "plateau", "valley", "canyon", "gorge", "pass", "tunnel", "cave",
    "forest", "woods", "jungle", "desert", "prairie", "plain", "field", "meadow", "pasture",
    "garden", "park", "reservation", "preserve", "sanctuary", "refuge", "haven", "oasis"
]

# For positions 17-18 (after "other side of")
boundary_words = [
    "the", "this", "that", "these", "those", "our", "your", "his", "her", "their", "its",
    "iron", "steel", "bamboo", "wooden", "concrete", "stone", "brick", "glass", "plastic",
    "curtain", "wall", "fence", "barrier", "border", "boundary", "frontier", "line", "divide",
    "world", "country", "nation", "state", "territory", "realm", "domain", "kingdom", "empire",
    "ocean", "sea", "river", "mountain", "range", "city", "town", "village", "desert", "forest",
    "globe", "earth", "land", "water", "air", "sky", "space", "universe"
]

# For positions 21-22 (after "at three")
time_words = [
    "am", "pm", "oclock", "o'clock", "hours", "hundred", "thirty", "minutes", "seconds",
    "in", "the", "morning", "afternoon", "evening", "night", "dawn", "dusk", "midnight",
    "noon", "midday", "sunrise", "sunset", "daybreak", "nightfall", "tomorrow", "today",
    "sharp", "exactly", "precisely", "approximately", "about", "around", "nearly", "almost"
]

# For position 42 (after "little yellow")
objects = [
    "house", "home", "cottage", "cabin", "shack", "hut", "tent", "apartment", "flat", "condo",
    "car", "truck", "van", "jeep", "suv", "vehicle", "automobile", "motorcycle", "bike", "bicycle",
    "airplane", "plane", "jet", "helicopter", "aircraft", "boat", "ship", "yacht", "submarine",
    "trailer", "camper", "rv", "motor", "book", "notebook", "notepad", "pad", "paper", "envelope",
    "card", "postcard", "letter", "message", "sign", "signal", "flag", "banner", "emblem", "symbol",
    "box", "case", "container", "jar", "bottle", "flask", "vial", "tube", "pipe", "bird", "dog", "cat",
    "pet", "animal", "creature", "flower", "plant", "tree", "bush", "shrub", "bag", "sack", "pouch",
    "pack", "backpack", "purse", "wallet", "handbag", "briefcase", "suitcase", "luggage", "hat",
    "cap", "helmet", "mask", "glasses", "goggles", "coat", "jacket", "sweater", "shirt", "pants",
    "shorts", "skirt", "dress", "suit", "uniform", "robe", "gown", "sheet", "blanket", "quilt",
    "umbrella", "parasol", "cane", "stick", "wand", "rod", "pole", "staff", "bat", "club", "racket",
    "ball", "disc", "frisbee", "toy", "game", "puzzle", "doll", "figure", "model", "statue", "sculpture",
    "painting", "drawing", "sketch", "portrait", "landscape", "still", "life", "abstract", "mural",
    "fresco", "mosaic", "collage", "photograph", "poster", "print", "calendar", "map", "chart", "graph",
    "diagram", "plan", "blueprint", "schematic", "design", "pattern", "template", "form", "format",
    "layout", "arrangement", "composition", "configuration", "structure", "construction", "building",
    "edifice", "tower", "castle", "palace", "mansion", "estate", "manor", "villa", "bungalow", "ranch",
    "farm", "barn", "shed", "garage", "carport", "hangar", "shelter", "refuge", "fortress", "bunker"
]

# For positions 43-53 (structure after "yellow [OBJECT]")
structure_words = [
    "and", "with", "that", "which", "where", "when", "while", "as", "like", "so", "but", "or",
    "nor", "yet", "for", "because", "since", "if", "unless", "until", "though", "although",
    "even", "read", "said", "stated", "wrote", "declared", "proclaimed", "announced", "revealed",
    "disclosed", "divulged", "confessed", "admitted", "acknowledged", "conceded", "granted",
    "sitting", "standing", "lying", "hanging", "floating", "flying", "moving", "running",
    "walking", "crawling", "climbing", "falling", "rising", "sinking", "turning", "spinning",
    "rotating", "revolving", "orbiting", "circling", "spiraling", "winding", "twisting",
    "bending", "folding", "curling", "coiling", "wrapping", "unwrapping", "opening", "closing",
    "stopping", "starting", "beginning", "ending", "finishing", "completing", "continuing",
    "proceeding", "advancing", "retreating", "withdrawing", "arriving", "departing", "leaving",
    "entering", "exiting", "coming", "going", "traveling", "journeying", "voyaging", "sailing",
    "cruising", "flying", "soaring", "gliding", "diving", "plunging", "dropping", "lifting",
    "raising", "lowering", "carrying", "holding", "supporting", "bearing", "containing",
    "including", "excluding", "omitting", "adding", "subtracting", "multiplying", "dividing",
    "calculating", "computing", "processing", "analyzing", "studying", "examining", "inspecting",
    "observing", "watching", "seeing", "viewing", "looking", "glancing", "peering", "staring",
    "gazing", "reading", "writing", "typing", "printing", "copying", "scanning", "faxing",
    "emailing", "messaging", "texting", "calling", "phoning", "ringing", "buzzing", "beeping",
    "alarming", "alerting", "warning", "cautioning", "notifying", "informing", "telling",
    "speaking", "talking", "chatting", "conversing", "discussing", "debating", "arguing",
    "disputing", "fighting", "battling", "warring", "struggling", "striving", "trying",
    "attempting", "endeavoring", "working", "laboring", "toiling", "straining", "pushing",
    "pulling", "dragging", "hauling", "lifting", "carrying", "toting", "lugging", "schlepping",
    "showing", "displaying", "exhibiting", "demonstrating", "illustrating", "indicating",
    "signifying", "representing", "symbolizing", "standing", "representing", "exemplifying",
    "typifying", "epitomizing", "incarnating", "embodying", "personifying", "characterizing",
    "depicting", "portraying", "describing", "narrating", "recounting", "relating", "telling",
    "stating", "saying", "uttering", "voicing", "expressing", "articulating", "pronouncing",
    "declaring", "proclaiming", "announcing", "heralding", "broadcasting", "publishing",
    "posting", "releasing", "issuing", "presenting", "delivering", "giving", "offering",
    "extending", "granting", "bestowing", "conferring", "awarding", "providing", "supplying",
    "furnishing", "equipping", "outfitting", "arming", "fortifying", "strengthening",
    "reinforcing", "supporting", "backing", "assisting", "helping", "aiding", "serving"
]

# For position 58 (same as position 11)
location_words = locations

# For positions 65-69 (around "forgive")
plea_words = [
    "please", "do", "just", "must", "should", "can", "may", "might", "could", "would", "will",
    "shall", "try", "to", "and", "but", "or", "if", "then", "now", "soon", "later", "today",
    "tomorrow", "forever", "always", "never", "again", "once", "twice", "thrice", "too", "also",
    "as", "well", "such", "so", "very", "truly", "really", "actually", "indeed", "certainly",
    "definitely", "absolutely", "completely", "entirely", "totally", "wholly", "fully", "greatly",
    "greatly", "sincerely", "honestly", "truly", "faithfully", "loyally", "devotedly", "all",
    "me", "my", "mine", "myself", "you", "your", "yours", "yourself", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "we", "us", "our", "ours", "ourselves",
    "they", "them", "their", "theirs", "themselves", "anyone", "everyone", "someone", "no", "one",
    "anybody", "everybody", "somebody", "nobody", "anything", "everything", "something", "nothing",
    "thank", "thankyou", "thanks", "appreciate", "grateful", "miss", "goodbye", "farewell", "adieu",
    "adios", "ciao", "sayonara", "so", "long", "cheerio", "au", "revoir", "until", "till", "we",
    "meet", "again", "godspeed", "good", "luck", "best", "wishes", "regards", "blessings", "prayers"
]

# For positions 73-76 (final words before "agent")
ending_words = [
    "your", "loyal", "faithful", "devoted", "dedicated", "committed", "trusted", "valued", "esteemed",
    "respected", "admired", "revered", "honored", "noble", "brave", "courageous", "valiant", "heroic",
    "fearless", "intrepid", "bold", "daring", "audacious", "adventurous", "former", "ex", "previous",
    "past", "old", "longtime", "veteran", "experienced", "seasoned", "trained", "skilled", "qualified",
    "competent", "capable", "able", "proficient", "expert", "master", "top", "chief", "head", "lead",
    "senior", "junior", "assistant", "deputy", "associate", "humble", "obedient", "good", "better",
    "best", "fine", "great", "excellent", "superb", "outstanding", "exceptional", "extraordinary",
    "remarkable", "phenomenal", "magnificent", "marvelous", "wonderful", "fantastic", "fabulous",
    "terrific", "tremendous", "stupendous", "incredible", "amazing", "astonishing", "astounding",
    "surprising", "shocking", "startling", "staggering", "stunning", "breathtaking", "awe-inspiring",
    "impressive", "imposing", "striking", "dramatic", "sensational", "american", "russian", "british",
    "french", "german", "italian", "spanish", "chinese", "japanese", "korean", "indian", "australian",
    "canadian", "mexican", "brazilian", "argentinian", "chilean", "peruvian", "colombian", "venezuelan",
    "ecuadorian", "bolivian", "paraguayan", "uruguayan", "panamanian", "costa", "rican", "nicaraguan",
    "honduran", "salvadoran", "guatemalan", "belizean", "cuban", "dominican", "haitian", "jamaican",
    "bahamian", "barbadian", "trinidadian", "tobagonian", "guyanese", "surinamese", "french", "guianese",
    "friend", "ally", "partner", "colleague", "associate", "companion", "comrade", "fellow", "brother",
    "sister", "father", "mother", "son", "daughter", "child", "parent", "spouse", "husband", "wife",
    "fiancé", "fiancée", "boyfriend", "girlfriend", "lover", "sweetheart", "darling", "dear", "beloved",
    "precious", "cherished", "treasured", "adored", "worshipped", "idolized", "deified", "exalted",
    "glorified", "always", "forever", "eternally", "everlastingly", "perpetually", "endlessly",
    "timelessly", "permanently", "constantly", "continually", "continuously", "unceasingly",
    "incessantly", "relentlessly", "persistently", "stubbornly", "tenaciously", "doggedly"
]

print("Starting the brute force search...")

# Try words for each specific position
position_word_map = {
    (0, 1, 2, 3, 4, 5): beginning_words,
    (11, 58): locations,
    (17, 18): boundary_words,
    (21, 22): time_words,
    42: objects,
    (43, 44, 45, 47, 49, 51, 52, 53): structure_words,
    (65, 66, 68, 69): plea_words,
    (73, 74, 75, 76): ending_words
}

for positions, word_list in position_word_map.items():
    if isinstance(positions, int):
        positions = (positions,)

    print(f"\nTrying {len(word_list)} words for position(s) {positions}...")
    start_time = time.time()

    for word in word_list:
        check_word(word)

    elapsed = time.time() - start_time
    print(f"Completed in {elapsed:.2f} seconds")

# Check for hash values that appear in multiple positions
print("\nChecking for repeated hashes...")
hash_count = {}
for pos, hash_val in target_hashes:
    hash_count[hash_val] = hash_count.get(hash_val, 0) + 1

repeated_hashes = {hash_val: count for hash_val, count in hash_count.items() if count > 1}
for hash_val, count in repeated_hashes.items():
    positions = [pos for pos, h in target_hashes if h == hash_val]
    print(f"Hash {hash_val[:8]}... appears at positions {positions}")

# Update decoded_words with new findings
decoded_words.update(new_words)

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

# Print the words we found in this run
if new_words:
    print("\nNewly found words:")
    for pos, word in sorted(new_words.items()):
        print(f"Position {pos}: {word}")

# Print all the known words to help manual analysis
all_words = set(decoded_words.values())
print("\nAll known words:")
for word in sorted(all_words):
    print(word)

# Write results to a file
with open("final_decoded_easy.txt", "w") as f:
    f.write(" ".join(message) + "\n\n")
    f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
    f.write("Key: " + key + "\n\n")
    f.write("All known words:\n")
    for word in sorted(all_words):
        f.write(word + "\n")
    f.write("\nRemaining unknown hashes:\n")
    for i in range(len(hashes)):
        if i not in decoded_words:
            f.write(f"{i}: {hashes[i]}\n")