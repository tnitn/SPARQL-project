from rdflib import Graph, URIRef, Literal


def read_turtle(filename):
    """
    Read the given .ttl file. (!) The file must be the result of https://github.com/acoli-repo/conll-rdf converting tool
    :param filename: the .ttl file
    :return: read .ttl file ready to be processed by Python
    """
    g = Graph()
    g.parse(filename)
    return g


def get_sents(graph):
    """
    Get all the pairs (id, sentence) of the file in a dictionary.
    Right now sentences are kept in a triple with a subject ending in "_0", predicate being "rdfs:comment", and object
    containing, among other information, text of the sentence which starts after "text = ". Accordingly, the unique id
    and the content of each sentence can be retrieved.
    :param graph: the parsed .ttl file
    :return: Dictionary of the format {id: sentence}
    """
    sents = dict()

    for s, o in graph.subject_objects(URIRef("http://www.w3.org/2000/01/rdf-schema#comment")):
        # get the id of the sentence without last "_0" as a key, and the content of the sentence as a value
        sents[s.split("conllu")[1][:-2]] = o.split("text = ")[1]
    return sents


def create_mod_ttl(graph, sentences, dest_name="trial.ttl"):
    """
    Modified .ttl file is created, each word ((and sentence)) instances now additionally containing
    predicate "conll:SENT" and object the content of the sentence it belongs to.
    It is done for easier retrieving every sentence during SPARQL querying.
    :param graph: the parsed .ttl file
    :param sentences: dictionary of the format {id: sentence}
    :param dest_name: the name of the new modified .ttl file. It is called "trial.ttl" by default
    :return: None
    """
    for s, p, o in graph:
        if o.n3(graph.namespace_manager) == "nif:Word" or o.n3(graph.namespace_manager) == "nif:Sentence":
            subj = s
            pred = URIRef("http://ufal.mff.cuni.cz/conll2009-st/task-description.html#SENT")  # conll:SENT
            obj = Literal(sentences[s.split("conllu")[1].split('_')[0]])  # sentence content
            graph.add((subj, pred, obj))
    graph.serialize(destination="{}".format(dest_name))


if __name__ == "__main__":
    pass
    # g = read_turtle("en_partut.ttl")
    # sents = get_sents(g)
    # create_mod_ttl(g, sents, "en_partut_adapted.ttl")
