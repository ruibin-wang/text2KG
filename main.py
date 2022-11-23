# This file is used to vist the OpenIE server, obtain the (entity,relationship,entity) pair
# This file running on the server side


# from stanfordcorenlp import StanfordCoreNLP
from pyopenie import OpenIE5
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher, NodeMatch
import neo4jupyter


######################################################################################
#### This part of code is used to test package of standfordcorenlp
# neo4jupyter.init_notebook_mode()
#
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j_test"))
# graph.run("Match (n) detach delete n")  ## clean the exist graph in the project
# node_matcher = NodeMatcher(graph)



# nlp = StanfordCoreNLP(r"D:\Code\text2KG\stanford_corenlp\stanford_corenlp")
# text = 'Guangdong University of foreign studies is located in Guangzhou'
# print(nlp.ner(text))
# print(nlp.pos_tag(text))
# print(nlp.dependency_parse(text))
# print(nlp.parse(text))
# print(nlp.annotate(text))

######################################################################################


# text = "Jack and Jill visited India, Japan and South Korea."
# text = "Niandra LaDes and Usually Just a T-Shirt is the debut album by the American musician John Frusciante, released on November 22, 1994, by American Recordings."
# text = "He and Galloway were among at least 10 Texas inmates with execution dates in the coming weeks."

text = "Mr. Miller said that it is 40 feet wide."

def Open_IE_output(text):

    extractor = OpenIE5('http://localhost:8000')
    extractions = extractor.extract(text)
    # print(extractions)

    return extractions


extractions = Open_IE_output(text)
entity_pair = []

for index in extractions:
    
    head_entity = index['extraction']['arg1']['text']
    relation = index['extraction']['rel']['text']
    tail_entiy = index['extraction']['arg2s'][0]['text']
    confidence = index['confidence']

    entity_pair.append([confidence, head_entity, relation, tail_entiy])


print(entity_pair)







