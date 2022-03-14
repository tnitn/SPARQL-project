from rdflib import Graph, URIRef, Literal


def read_turtle(filename):
    """
    Read the given .ttl file. (!) The file must be the result of "turtle_changer.py" modifying tool
    :param filename: the .ttl file
    :return: read .ttl file ready to be processed by Python
    """
    graph = Graph()
    graph.parse(filename)
    return graph


def lemma(g, lemma):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent
        WHERE {
          ?s conll:LEMMA ?lemma;
             conll:SENT ?sent
        }
    """
    for r in g.query(q, initBindings={'lemma': Literal(lemma)}):
        yield r["sent"]


def regex(g, pattern):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent
        WHERE {
          ?s conll:WORD ?word;
             conll:SENT ?sent .
          FILTER regex(?word, ?pat)
        }
    """
    for r in g.query(q, initBindings={'pat': Literal(pattern)}):
        yield r["sent"]


def word1_or_word2(g, word1, word2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        SELECT ?sent1 ?sent2
        WHERE {
          {?s conll:WORD ?word1;
              conll:SENT ?sent1}
          UNION
          {?s conll:WORD ?word2;
              conll:SENT ?sent2}
        }
    """
    for r in g.query(q, initBindings={'word1': Literal(word1), 'word2': Literal(word2)}):
        yield r["sent1"] if r["sent1"] else r["sent2"]


def word1_or_word2_or_word3(g, word1, word2, word3):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        SELECT ?sent1 ?sent2 ?sent3
        WHERE {
          {?s conll:WORD ?word1;
              conll:SENT ?sent1}
          UNION
          {?s conll:WORD ?word2;
              conll:SENT ?sent2}
          UNION
          {?s conll:WORD ?word3;
              conll:SENT ?sent3}
        }
    """
    for r in g.query(q, initBindings={'word1': Literal(word1), 'word2': Literal(word2), 'word3': Literal(word3)}):
        yield r["sent1"] if r["sent1"] else r["sent2"] if r["sent2"] else r["sent3"]


if __name__ == "__main__":
    gr = read_turtle("trial.ttl")

    # for sent in lemma(gr, "daily"):
    #     print(sent)

    # for sent in regex(gr, "^u."):
    #     print(sent)

    for sent in word1_or_word2(gr, "tuesday", "thursday"):
        print(sent)

    # for sent in word1_or_word2_or_word3(gr, "tuesday", "thursday", "saturday"):
    #     print(sent)
