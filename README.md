# SPARQL-project

## Introduction
The aim of this project is to compare the efficiency of TüNDRA (.conllu) web tool and SPARQL (.ttl) query language for retrieving data from linguistic treebanks. This repository contains the shortened version of the research; for the more detailed version please access *name of the paper*.  

### Material
The same databank *UD English-ParTUT* was used to illustrate the difference in queries. According to [Universal Dependencies website](https://universaldependencies.org/), this treebank is a conversion of a multilingual parallel treebank which was developed at the University of Turin, and it is made of a different kinds of texts such as legal texts, talks and articles from Wikipedia, among others. The .conllu version was accessed directly via [Tündra web tool.](https://weblicht.sfs.uni-tuebingen.de/Tundra/) The .ttl version was first downloaded from the [Universal Dependencies website](https://universaldependencies.org/) in the .conllu format, and then transformed into .ttl format with the help of [ConLL-RDF tool](https://github.com/acoli-repo/conll-rdf) ([en_partut.ttl](en_partut.ttl)). Some further changes were then made to the .ttl file which will be further described in the Description section, with the final file used for querying being [en_partut_adapted.ttl](en_partut_adapted.ttl).

## Description
### .ttl adaptation
To make the outputs of two applications more similar, it is important that SPARQL queries will return the whole sentences and not only the word/lemma/etc., as this is how the output is provided by TüNDRA. The original .ttl file doesn't have a direct reference from a word to the sentence it belongs to, so it was decided to add to every *subject* (that contains an object *nif:Word*)? another pair of a predicate-object, namely *"conll:SENT \*sentence\*"* which were retrieved from a *rdfs:comment* predicate. Please refer to [turtle_changer.py](turtle_changer.py) for more detailed information and specific methods used. Important, the *turtle_changer.py* file can be used for any .ttl file generated by the aforementioned conllu-rdf tool.

### Queries comparison
Below can be found queries searching for the same information. All the screenshots of TüNDRA web tool examples are taken from the [TüNDRA Tutorial](https://weblicht.sfs.uni-tuebingen.de/Tundra/tutorial) and [UD English ParTUT](https://weblicht.sfs.uni-tuebingen.de/Tundra/UD_English-ParTUT_v2.4/). For SPARQL queries Apache Jena Fuseki was used. Templates for the SPARQL queries wih the possibility to change the exact instance searched and copy the queries can be found in [sparql_queries.py](sparql_queries.py).

| lemma_TüNDRA | lemma_SPARQL |
-------------- | --------------
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/lemma.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/lemma.png) |
| **regex_TüNDRA** | **regex_SPARQL**  |
| \[word = /.\*able/\] | PREFIX conll: <<http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:WORD ?word; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent . <br> &nbsp; FILTER regex(?word, ".\*able$") <br> } |
| **word1_xor_word2_Tündra** | **word1_xor_word2_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/word1XorWord2.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/word1XorWord2.png) |
| **pos_and_lemma_TüNDRA** | **pos_and_lemma_SPARQL** |
| \[pos = "NOUN" & lemma = /un.\*/\] | PREFIX conll: <<http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:POS_COARSE "NOUN"; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:LEMMA ?lemma; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent . <br> &nbsp; FILTER regex(lemma, "^un.\*") <br> } |
| **adj_word1_and_word2_TüNDRA** | **adj_word1_and_word2_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/word1_adj_word2.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/word1_adj_word2.png) |
| **words_atadistance_2_TüNDRA** | **words_atadistance_2_SPARQL** |
| \[word = "the"\] .2 \[word = "world"\] | PREFIX conll: <<http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>> <br> PREFIX nif: <<http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#>> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s a nif:Sentence; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent <br> &nbsp; FILTER (regex(?sent, "\\\bthe \\\w+ world\\\b")) <br> } |
| **words_atadistance_2or3_TüNDRA** | **words_atadistance_2or3_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/words_atadistance_2or3.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/words_aradistance_2or3.png) |
| **words_at_any_distance_TüNDRA** | **words_at_any_distance_SPARQL** |
| \[word = "he"\] .* \[word = "to"\] | PREFIX conll: <<http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>> <br> PREFIX nif: <<http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#>> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s a nif:Sentence; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent <br> &nbsp; FILTER (regex(?sent, "\\\bhe\\\b.\*\\\bto\\\b")) <br> } |
| **adj_pos1_and_pos2_TüNDRA** | **adj_pos1_and_pos2_SPARQL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/adj_pos1_and_pos2.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/adj_pos1_and_pos2.png) |
| **word1_headOf_word2_TüNDRA** | **word1_headOf_word2_SPARQL** |
| \[word = "see"\] > \[word = "we"\] | PREFIX conll: <<http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:WORD "see" . <br> &nbsp; ?s1 conll:HEAD ?s; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:WORD "we"; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent <br> } |
| **pos1_headOf_word2_edge_TüNDRA** | **pos1_headOf_word2_edge_SPAQRL** |
| ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/T%C3%BCNDRA%20screenshots/pos1_word2_edge.png) | ![](https://github.com/tnitn/SPARQL-project/blob/main/screenshots/SPARQL%20screenshots/pos1_word2_edge.png) |
| **pos1_headOf_not_pos2_TüNDRA** | **pos1_headOf_not_pos2_SPARQL** |
| \[pos="PROPN"\] !> \[pos="ADP"\] | PREFIX conll: <<http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>> <br><br> SELECT ?sent <br> WHERE { <br> &nbsp; ?s conll:POS_COARSE "PROPN"; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:SENT ?sent . <br> &nbsp; ?s1 conll:HEAD ?s; <br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; conll:POS_COARSE ?pos; <br> &nbsp; FILTER (?pos != "ADP") <br> } |

## Limitations
All in all, quering information given above showed a good result as all the (major) TüNDRA queries can be reproduced in SPARQL. Although TüNDRA syntax is arguably more straightforward and easier to learn than SPARQL syntax, for those who are more used to quering in SPARQL and are advanced in this language, this may appear otherwise. \
However, the major disadvantage of SPARQL queries is the limitation of information being possible to retrieve. In comparison to SPARQL, TüNDRA was specifically created for querying linguistic dependency and constituency treebanks, and apart from displaying sentences, it also displays the corresponding tree; table view of each word of the sentence, attributes of which can be added to or deleted from this table "in a click"; statistics of the attributes; as well as another table for showing the table in context. The output of "Statistics" and "Table View" can also be regulated via query itself which is also not available in SPARQL.

## Output
The conclusion to draw is that the efficiency of SPARQL is to be improved. For example, natural further development for this topic would be creation and introduction of extra web tools for SPARQL that would allow to visualise the output or even build corresponding linguistic trees. However, the current research proved that it is already possible to use SPARQL syntax for the successful search of desired data.

## References
* Scott Martens (2013). TüNDRA: A Web Application for Treebank Search and Visualization. In: Proceedings of The Twelfth Workshop on Treebanks and Linguistic Theories (TLT12), Sofia, pp. 133—144. URL: http://bultreebank.org/TLT12/TLT12Proceedings.pdf
* Chiarcos C., Fäth C. (2017), CoNLL-RDF: Linked Corpora Done in an NLP-Friendly Way. In: Gracia J., Bond F., McCrae J., Buitelaar P., Chiarcos C., Hellmann S. (eds) Language, Data, and Knowledge. LDK 2017. pp 74-88. 
