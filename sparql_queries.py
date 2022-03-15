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


def pos(g, pos):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>

        SELECT ?sent
        WHERE {
          ?s conll:POS_COARSE ?pos;
             conll:SENT ?sent
        }
    """
    for r in g.query(q, initBindings={'pos': Literal(pos)}):
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


def word1_xor_word2(g, word1, word2):
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


def word1_xor_word2_xor_word3(g, word1, word2, word3):
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


def feat1_and_feat2(g, f1, f2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent
        WHERE {
          ?s conll:POS_COARSE ?f1;
             conll:WORD ?word;
             conll:SENT ?sent .
          FILTER regex(?word, ?f2)
        }
    """
    for r in g.query(q, initBindings={'f1': Literal(f1), 'f2': Literal(f2)}):
        yield r["sent"]


def word1_and_word2_unord(g, w1, w2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        PREFIX nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#>
        
        SELECT ?sent
        WHERE {
          ?s a nif:Sentence;
             conll:SENT ?sent
          FILTER (regex(?sent, ?w1) && regex(?sent, ?w2))
        }
    """
    for r in g.query(q, initBindings={'w1': Literal(w1), 'w2': Literal(w2)}):
        yield r["sent"]


def word1_and_word2_adj(g, w1, w2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        PREFIX nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#>
        
        SELECT ?sent
        WHERE {
          ?s a nif:Sentence;
             conll:SENT ?sent
          FILTER (regex(?sent, ?seq))
        }
    """
    seq = ' '.join((w1, w2))
    for r in g.query(q, initBindings={'seq': Literal(seq)}):
        yield r["sent"]


def word1_and_word2_ord(g, w1, w2, start, end=-1):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        PREFIX nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#>

        SELECT ?sent
        WHERE {
          ?s a nif:Sentence;
             conll:SENT ?sent
          FILTER (regex(?sent, ?pat))
        }
    """
    pat = f'{w1} (\\w+ ){{{start}}}{w2}'
    if end != -1:
        pat = f'{w1} (\\w+ ){{{start},{end}}}{w2}'
    for r in g.query(q, initBindings={'pat': Literal(pat)}):
        yield r["sent"]


def feat1_and_feat2_adj(g, f1, f2):
    pass


if __name__ == "__main__":
    gr = read_turtle("trial.ttl")

    # for sent in lemma(gr, "daily"):
    #     print(sent)
    #
    # for sent in pos(gr, "ADP"):
    #     print(sent)
    #
    # for sent in regex(gr, "^u."):
    #     print(sent)
    #
    # for sent in word1_xor_word2(gr, "tuesday", "thursday"):
    #     print(sent)
    #
    # for sent in word1_xor_word2_xor_word3(gr, "tuesday", "thursday", "saturday"):
    #     print(sent)
    #
    # for sent in feat1_and_feat2(gr, "NOUN", "un.*"):
    #     print(sent)

    # for sent in word1_and_word2_unord(gr, "flights", "are"):
    #     print(sent)

    # for sent in word1_and_word2_adj(gr, "flights", "are"):
    #     print(sent)

    for sent in word1_and_word2_ord(gr, "are", "flights", 1, 2):
        print(sent)
