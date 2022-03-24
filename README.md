# SPARQL-project

## Introduction
The aim of this project is to compare the efficiency of TüNDRA (.conllu) and SPARQL (.ttl) query languages for retrieving data from linguistic treebanks.

### Material
The same databank *English-ParTUT* was used to illustrate the difference in queries. The .conllu treebank was accessed directly via [Tündra web tool.](https://weblicht.sfs.uni-tuebingen.de/Tundra/) The .ttl treebank was first downloaded from the [Universal Dependencies website](https://universaldependencies.org/) in the .conllu format, and then transformed into .ttl format with the help of [ConLL-RDF tool.](https://github.com/acoli-repo/conll-rdf) Some further changes were then made to the .ttl file which will be further described in the Description section.

## Description
### .ttl adaptation
To make the outputs of two query languages more similar, it is important that SPARQL queries will return the whole sentences. The original .ttl file doesn't have a direct reference from a word to the sentence it belongs to, so it was decided to add to every *subject* (that contains an object *nif:Word*)? another pair of a predicate-object, namely *"conll:SENT \*sentence\*"* which were retrieved from a *rdfs:comment* predicate. Please refer to [turtle_changer.py](*turtle_changer.py*) for more detailed information and specific methods used. Important, the *turtle_changer.py* file can be used for any .ttl file generated by the aforementioned conllu-rdf tool.

### Queries comparison
Below can be found queries searching for the same information. All the screenshots of TüNDRA query examples are taken from the [TüNDRA Tutorial](https://weblicht.sfs.uni-tuebingen.de/Tundra/tutorial). Templates for the SPARQL queries wih the possibility to change the exact instance searched can be found in [sparql_queries.py](sparql_queries.py).

| lemma_TüNDRA | lemma_SPARQL |
-------------- | --------------
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/lemma.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/lemma.png) |
| **regex_TüNDRA** | **regex_SPARQL**  |
| \[word = /.\*able/\] | PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:WORD ?word; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent . <br> &nbsp; FILTER regex(?word, ".\*able") <br> } |

## Conclusion

## References
* Scott Martens (2013). TüNDRA: A Web Application for Treebank Search and Visualization. In: Proceedings of The Twelfth Workshop on Treebanks and Linguistic Theories (TLT12), Sofia, pp. 133—144. URL: http://bultreebank.org/TLT12/TLT12Proceedings.pdf
* Chiarcos C., Fäth C. (2017), CoNLL-RDF: Linked Corpora Done in an NLP-Friendly Way. In: Gracia J., Bond F., McCrae J., Buitelaar P., Chiarcos C., Hellmann S. (eds) Language, Data, and Knowledge. LDK 2017. pp 74-88.
