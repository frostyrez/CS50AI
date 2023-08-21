# Parser

Write an AI to parse sentences and extract noun phrases.

<img width="700" alt="image" src="https://github.com/frostyrez/CS50AI/assets/123249055/981d75b6-0209-403d-8d86-264cc21290b9">

## Outline

- Vocabulary and grammar rules are initially defined, with `TERMINALS` defining the word type (adjective, noun, etc) and `NONTERMINALS` defining sentence structures (a sentence can be a noun phrase + verb phrase).
- Once the sentence has been defined, it is fed into `preprocess`, which tokenizes the word, i.e. returns a lowercased list of the words in the sentence.
- `np_chunk` then traverses the `nltk tree` for "noun phrase chunks", i.e. noun phrases that do not themselves contain noun phrases.

## Usage

Run `pip3 install -r requirements.txt` to install `nltk`, a natural language processing library.

`python parser1.py sentences/1.txt` will use a pre-defined sentence.

`python parser1.py` will prompt you for a sentence to parse. (Note that grammar rules and parsing are limited to the words contained in `TERMINALS`)

Sentences 1-10 provided.
