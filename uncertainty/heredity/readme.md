# Heredity

Assess likelihood that each person will have a particular genetic trait given their parents' genetic information

<img width="563" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/b23fac29-895c-4fe2-a18c-55869b6f7bc7">

## Outline

- The probability that a child exhibits a specific trait depends on whether the likelihood of them having X genes, which depends on the number of copies of the gene in each of its parents. This can be modelled by the following Bayesian Network:
  
<img width="600" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/53e5df73-ff5c-4ef6-8ae1-75a36ed21cf8">

- These probabilities are defined as such:

  <img width="326" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/626b9d3a-5a58-4307-9f41-67f4cff7048d">

  With unconditional probabilities used if parent information not available, and mutation probability representing the possibility of "receiving" a gene from a parent who has 0 copies of the gene (and vice-versa).

- A joint probabilty is then calculated which takes into account all these eventualities, normalises them, and outputs each family members probability of having 0, 1, and 2 genes and their probability of exhibiting the trait or not.

## Usage

`python heredity.py data/family0.csv`  
  
`family1.csv` and `family2.csv` also provided.
