# SPARQL-project

## Introduction
The aim of this project is to compare the efficiency of TüNDRA (.conllu) and SPARQL (.ttl) query languages for retrieving data from linguistic treebanks.

### Material
The same databank *name* was used to illustrate the difference in queries. The .conllu treebank was accessed directly via [Tündra web tool.](https://weblicht.sfs.uni-tuebingen.de/Tundra/) The .ttl treebank was first downloaded from the [Universal Dependencies website](https://universaldependencies.org/) in the .conllu format, and then transformed into .ttl format with the help of [ConLL-RDF tool.*](https://github.com/acoli-repo/conll-rdf) Some further changes were then made to the .ttl file which will be further described in the Description section.

## Description
### .ttl adaptation
To make the outputs of two query languages more similar, it is important that SPARQL queries will return the whole sentences. The original .ttl file doesn't have a direct reference from a word to the sentence it belongs to, so it was decided to add to every *subject* (that contains an object *nif:Word*)? another pair of a predicate-object, namely *"conll:SENT \*sentence\*"* which were retrieved from a *rdfs:comment* predicate. Please refer to *turtle_changer.py* for more detailed information and specific methods used.

## References
* Chiarcos C., Fäth C. (2017), CoNLL-RDF: Linked Corpora Done in an NLP-Friendly Way. In: Gracia J., Bond F., McCrae J., Buitelaar P., Chiarcos C., Hellmann S. (eds) Language, Data, and Knowledge. LDK 2017. pp 74-88.
