import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Create dictionary with probabilities
    probs = dict.fromkeys(corpus)
    for prob in probs:
        probs[prob] = 0

    # Apply probs
    for subpage in corpus[page]:
        probs[subpage] = damping_factor / len(corpus[page])
    for p in corpus:
        probs[p] += (1-damping_factor) / len(corpus)

    return probs   


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initalise PageRank
    pr = dict.fromkeys(corpus)
    for p in pr:
        pr[p] = 0

    # Choose page from corpus at random
    page = random.choice(list(corpus.keys()))

    # Sample loop
    for i in range(n):
        prob_dist = transition_model(corpus,page,damping_factor)
        page = random.choices(list(prob_dist.keys()),weights=list(prob_dist.values()))
        page = page[0]
        pr[page] += 1
    for p in pr:
        pr[p] /= n
    
    return pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initalise PageRank
    pr = dict.fromkeys(corpus)
    for page in pr:
        pr[page] = 1 / len(pr)
    

    # Initialise linked dictionary
    linked = dict.fromkeys(corpus)
    for k in linked:
        linked[k] = set()
    for k,v in corpus.items():
        for subv in v:
            linked[subv].add(k)

    # Init params
    c = .001
    d = damping_factor
    max_diff = 1

    while max_diff > c:
        pr_old = copy.deepcopy(pr)
        diffs = dict.fromkeys(pr)
        for page in pr:
            sum = 0
            for l in linked[page]:
                sum += pr[l]/len(corpus[l])
            pr[page] = (1-d)/len(pr) + d * sum
            diffs[page] = abs(pr[page]-pr_old[page])
        max_diff = max(diffs.values())

    return pr
    

if __name__ == "__main__":
    main()
