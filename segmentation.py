import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# connectors that usually create scene splits
CONNECTORS = {
    "and", "but", "so", "then", "after", "before",
    "because", "while", "when", "although", "however"
}


def split_clauses(sentence):
    """
    Use dependency parsing to split sentence into action-based clauses
    """

    doc = nlp(sentence)

    clauses = []
    current_clause = []

    for token in doc:

        # detect clause boundaries
        if token.dep_ in ("cc", "conj", "advcl") and current_clause:
            clauses.append(" ".join([t.text for t in current_clause]).strip())
            current_clause = []

        current_clause.append(token)

    if current_clause:
        clauses.append(" ".join([t.text for t in current_clause]).strip())

    return clauses


def clean_clause(clause):
    """
    Remove connectors and small fragments
    """

    words = clause.split()

    if words and words[0].lower() in CONNECTORS:
        words = words[1:]

    return " ".join(words).strip()


def refine_clauses(clauses):
    """
    Merge fragments that are too short
    """

    refined = []

    for clause in clauses:

        clause = clean_clause(clause)

        # skip empty clauses
        if not clause:
            continue

        words = clause.split()

        # merge tiny fragments
        if len(words) < 4 and refined:
            refined[-1] = refined[-1] + " " + clause
        else:
            refined.append(clause)

    return refined


def enforce_scene_limits(scenes, min_scenes=3, max_scenes=7):
    """
    Ensure scene count stays between limits
    """

    # too few scenes → split longest scene
    while len(scenes) < min_scenes:

        longest_index = max(range(len(scenes)), key=lambda i: len(scenes[i]))

        words = scenes[longest_index].split()

        midpoint = len(words) // 2

        part1 = " ".join(words[:midpoint])
        part2 = " ".join(words[midpoint:])

        scenes[longest_index] = part1
        scenes.insert(longest_index + 1, part2)

    # too many scenes → merge adjacent
    while len(scenes) > max_scenes:

        scenes[-2] = scenes[-2] + " " + scenes[-1]
        scenes.pop()

    return scenes


def segment_story(text):
    """
    Main segmentation pipeline
    """

    doc = nlp(text)

    # Step 1: sentence segmentation
    sentences = [sent.text.strip() for sent in doc.sents]

    clauses = []

    # Step 2: clause segmentation
    for sentence in sentences:
        clauses.extend(split_clauses(sentence))

    # Step 3: refine clauses
    scenes = refine_clauses(clauses)

    # Step 4: enforce limits
    scenes = enforce_scene_limits(scenes)

    return scenes