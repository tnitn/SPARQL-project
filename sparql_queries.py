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


# (!) extremely slow in Python
def pos1_and_pos2_adj(g, pos1, pos2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        
        SELECT ?sent1
        WHERE {
          ?s1 conll:POS_COARSE ?pos1;
              conll:ID ?id1;
              conll:SENT ?sent1.
          ?s2 conll:POS_COARSE ?pos2;
              conll:ID ?id2;
              conll:SENT ?sent2.
          FILTER (xsd:integer(?id1)+1 = xsd:integer(?id2) && ?sent1 = ?sent2)
        }    
    """
    for r in g.query(q, initBindings={'pos1': Literal(pos1), 'pos2': Literal(pos2)}):
        yield r["sent1"]


def word1_headOf_word2(g, w1, w2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent
        WHERE {
          ?s conll:WORD ?word1 .
          ?s1 conll:HEAD ?s;
              conll:WORD ?word2;
              conll:SENT ?sent
        }
    """
    for r in g.query(q, initBindings={'word1': Literal(w1), 'word2': Literal(w2)}):
        yield r["sent"]


def lemma1_headOf_word2_edge(g, l1, w2, edge):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent
        WHERE {
          ?s conll:LEMMA ?lemma1 .
          ?s1 conll:HEAD ?s;
              conll:WORD ?word2;
              conll:EDGE ?edge;
              conll:SENT ?sent
        }
    """
    for r in g.query(q, initBindings={'lemma1': Literal(l1), 'word2': Literal(w2), 'edge': Literal(edge)}):
        yield r["sent"]


def word1_headOf_word2_edge1_or_edge2(g, w1, w2, e1, e2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent1 ?sent2
        WHERE {
          ?s conll:WORD ?word1 .
          {?s1 conll:HEAD ?s;
              conll:WORD ?word2;
              conll:EDGE ?edge1;
              conll:SENT ?sent1 .}
          UNION
          {?s2 conll:HEAD ?s;
              conll:WORD ?word2;
              conll:EDGE ?edge2;
              conll:SENT ?sent2 .}
        }
    """
    for r in g.query(q, initBindings={'word1': Literal(w1), 'word2': Literal(w2),
                                      'edge1': Literal(e1), 'edge2': Literal(e2)}):
        yield r["sent1"] if r["sent1"] else r["sent2"]


def pos1_headOfhead_word2(g, p1, w2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent
        WHERE {
          ?s conll:POS_COARSE ?pos1 .
          ?s1 conll:HEAD ?s .
          ?s2 conll:HEAD ?s1;
              conll:WORD ?word2;
              conll:SENT ?sent .
        }
    """
    for r in g.query(q, initBindings={'pos1': Literal(p1), 'word2': Literal(w2)}):
        yield r["sent"]


def pos1_headOf_not_pos2(g, p1, p2):
    q = """
        PREFIX conll: <http://ufal.mff.cuni.cz/conll2009-st/task-description.html#>
        
        SELECT ?sent
        WHERE {
          ?s conll:POS_COARSE ?pos1;
             conll:WORD ?word .
          ?s1 conll:HEAD ?s;
              conll:POS_COARSE ?pos;
              conll:SENT ?sent .
          FILTER (?pos != ?pos2)
        }
    """
    for r in g.query(q, initBindings={'pos1': Literal(p1), 'pos2': Literal(p2)}):
        yield r["sent"]


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

    # for sent in word1_and_word2_ord(gr, "are", "flights", 1, 2):
    #     print(sent)

    # # extremely slow
    # # for sent in pos1_and_pos2_adj(gr, "DET", "PROPN"):
    # #     print(sent)

    # for sent in lemma1_headOf_word2(gr, "boston", "from"):
    #     print(sent)

    # for sent in word1_headOf_word2_edge(gr, "flights", "daily", "amod"):
    #     print(sent)

    # for sent in word1_headOf_word2_edge1_or_edge2(gr, "flights", "daily", "amod", "cmod"):
    #     print(sent)

    # for sent in pos1_headOfhead_word2(gr, "VERB", "daily"):
    #     print(sent)

    for sent in pos1_headOf_not_pos2(gr, "PROPN", "ADP"):
        print(sent)
