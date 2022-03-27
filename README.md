# SPARQL-project

## Introduction
The aim of this project is to compare the efficiency of TüNDRA (.conllu) and SPARQL (.ttl) query languages for retrieving data from linguistic treebanks.

### Material
The same databank *UD English-ParTUT* was used to illustrate the difference in queries. The .conllu treebank was accessed directly via [Tündra web tool.](https://weblicht.sfs.uni-tuebingen.de/Tundra/) The .ttl treebank was first downloaded from the [Universal Dependencies website](https://universaldependencies.org/) in the .conllu format, and then transformed into .ttl format with the help of [ConLL-RDF tool](https://github.com/acoli-repo/conll-rdf) ([en_partut.ttl](en_partut.ttl)). Some further changes were then made to the .ttl file which will be further described in the Description section, with the final file used for querying being [en_partut_adapted.ttl](en_partut_adapted.ttl).

## Description
### .ttl adaptation
To make the outputs of two query languages more similar, it is important that SPARQL queries will return the whole sentences. The original .ttl file doesn't have a direct reference from a word to the sentence it belongs to, so it was decided to add to every *subject* (that contains an object *nif:Word*)? another pair of a predicate-object, namely *"conll:SENT \*sentence\*"* which were retrieved from a *rdfs:comment* predicate. Please refer to [turtle_changer.py](*turtle_changer.py*) for more detailed information and specific methods used. Important, the *turtle_changer.py* file can be used for any .ttl file generated by the aforementioned conllu-rdf tool.

### Queries comparison
Below can be found queries searching for the same information. All the screenshots of TüNDRA query examples are taken from the [TüNDRA Tutorial](https://weblicht.sfs.uni-tuebingen.de/Tundra/tutorial) and [UD English ParTUT](https://weblicht.sfs.uni-tuebingen.de/Tundra/UD_English-ParTUT_v2.4/). Templates for the SPARQL queries wih the possibility to change the exact instance searched and copy the queries can be found in [sparql_queries.py](sparql_queries.py).

| lemma_TüNDRA | lemma_SPARQL |
-------------- | --------------
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/lemma.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/lemma.png) |
| **regex_TüNDRA** | **regex_SPARQL**  |
| \[word = /.\*able/\] | PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:WORD ?word; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent . <br> &nbsp; FILTER regex(?word, ".\*able") <br> } |
| **word1_xor_word2_Tündra** | **word1_xor_word2_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/word1XorWord2.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/word1XorWord2.png) |
| **pos_and_lemma_TüNDRA** | **pos_and_lemma_SPARQL** |
| \[pos = "NOUN" & lemma = /un.\*/\] | PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:POS_COARSE "NOUN"; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:LEMMA ?lemma; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent . <br> &nbsp; FILTER regex(lemma, "^un.\*") <br> } |
| **adj_word1_and_word2_TüNDRA** | **adj_word1_and_word2_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/word1_adj_word2.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/word1_adj_word2.png) |
| **words_atadistance_2_TüNDRA** | **words_atadistance_2_SPARQL** |
| \[word = "the"\] .2 \[word = "world"\] | PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#> <br> PREFIX nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s a nif:Sentence; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent <br> &nbsp; FILTER (regex(?sent, "\\\bthe \\\w+ world\\\b")) <br> } |
| **words_atadistance_2or3_TüNDRA** | **words_atadistance_2or3_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/words_atadistance_2or3.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/words_aradistance_2or3.png) |
| **words_at_any_distance_TüNDRA** | **words_at_any_distance_SPARQL** |
| \[word = "he"\] .* \[word = "to"\] | PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#> <br> PREFIX nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s a nif:Sentence; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent <br> &nbsp; FILTER (regex(?sent, "\\bhe\\b.\*\\bto\\b")) <br> } |
| **adj_pos1_and_pos2_TüNDRA** | **adj_pos1_and_pos2_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/adj_pos1_and_pos2.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/adj_pos1_and_pos2.png) |
| **word1_headOf_word2_TüNDRA** | **word1_headOf_word2_SPARQL** |
| \[word = "see"\] > \[word = "we"\] | PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:WORD "see" . <br> &nbsp; ?s1 conll:HEAD ?s; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:WORD "we"; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent <br> } |
| **pos1_headOf_word2_edge_TüNDRA** | **lemma1_headOf_word2_edge_SPAQRL** |


## Conclusion

## References
* Scott Martens (2013). TüNDRA: A Web Application for Treebank Search and Visualization. In: Proceedings of The Twelfth Workshop on Treebanks and Linguistic Theories (TLT12), Sofia, pp. 133—144. URL: http://bultreebank.org/TLT12/TLT12Proceedings.pdf
* Chiarcos C., Fäth C. (2017), CoNLL-RDF: Linked Corpora Done in an NLP-Friendly Way. In: Gracia J., Bond F., McCrae J., Buitelaar P., Chiarcos C., Hellmann S. (eds) Language, Data, and Knowledge. LDK 2017. pp 74-88.
