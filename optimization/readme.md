# Optimization

Generate words for a crossword puzzle given a structure and a dictionary.
<img width="900" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/09fa792c-f280-44bb-896f-4df57b69dad2">
<img width="150" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/29fec47f-924b-4651-8528-f9e53f462377">

## Outline

- This problem is modelled as a constraint satisfaction problem, with both unary constraints (word length) and binary constraints (overlap with other words). Each word chosen to fill a `Variable` object must satisfy all unary and binary constraints imposed upon it.
- With each row and column containing a `domains` property consisting of the entire list of words, node consistency is initially enforced, whereby `domains` is reduced to words with the correct length.
- Arc consistency (satisfying all binary constraints) is then enforced by means of `ac3`, which takes into account all neighbors within each variable's `overlaps` property.
- `ac3` is called within the context of `backtrack`, a backtracking search which takes as input a partial assignment for the crossword and returns a complete assignment (if possible).

## Usage
`python generate.py data/structure0.txt data/words0.txt`

`structure1`, `structure2`, `words1`, and `words2` also provided.  
  
Try different structure/words combinations!
