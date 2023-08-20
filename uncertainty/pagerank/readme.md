# PageRank

Rank web pages within a corpus using either the Random Surfer Model or an iterative equation-based algorithm.

<img width="512" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/bcfe1bdc-2862-4bb8-8061-857cb31fbc69">

## Outline

- Two different methods are employed to estimate the PageRank of each page:
  - Sampling, aka "Random Surfer Model", simulates a surfer who starts on a random web page, then randomly clicks on a link in that web page. The PageRank is then calculated as the probability that a random surfer is on that page at any given time.
  - The iterative algorithm, based on the recursive mathematical expression shown below, calculates PageRank as a function of the PageRanks of all other pages that link to it.
$$PR(p) = \frac{1-d}{N} + d \sum_{i} \frac{PR(i)}{NumLinks(i)}$$
  where $d$ is a damping factor, $N$ is the total number of pages in the corpus, $i$ ranges over all pages that link to page $p$, and $NumLinks(i)$ is the number of links present on page $i$.
  This process is repeated until all PageRanks have sufficiently converged.

## Usage

`python pagerank.py corpus0`  
  
`corpus1` and `corpus2` also provided.
