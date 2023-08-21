import nltk
# works with "She never said a word until we were at the door here."
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Conj VP
NP -> N | NP PP | AP NP | Det NP
VP -> V | V PP | V NP | V NP PP | VP Adv | Adv VP
PP -> P NP | P S
AP -> Adj | Adj AP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    #for tree in trees:
    tree = trees[0]
    tree.pretty_print()

    print("Noun Phrase Chunks")
    for np in np_chunk(tree):
        print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokens = nltk.word_tokenize(sentence)
    for i, token in enumerate(tokens):
        if ord(token[0])>64 and ord(token[0])<91: # if 1st letter uppercase, make lowercase
            tokens[i] = chr(ord(token[0])+32) + token[1:]
        elif not (ord(token[0])>96 and ord(token[0])<123): # if not lowercase letter, return false
            tokens.remove(token)
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP' and not contains_nps(subtree):
            chunks.append(subtree)
    # for subtree in tree.subtrees():
    #     if subtree.label() == 'NP':
    #         labels = []
    #         for leaf in subtree:
    #             labels.append(leaf.label())
    #         if all(label != 'NP' for label in labels):
    #             chunks.append(subtree[0][0])            
    return chunks

def contains_nps(tree):
    for subtree in tree.subtrees():
        if subtree != tree and subtree.label() == 'NP':
            return True
    return False


if __name__ == "__main__":
    main()
