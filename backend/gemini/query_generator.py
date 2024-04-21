import json
from backend.memgraph.db_operations import get_topics
from backend.memgraph.database.memgraph import Memgraph



# ======================== WRITING CYPHER QUERIES ========================

# take in a json string of the form in data_format.json file and produce a cypher query to insert the data into the graph with a uuid

def topic_cypher_query(topic):
    f = open("../backend/resources/gemini_data.txt", "w+")
    topic_query = f"CREATE (n:Topic {{ id: '{topic.name}', description: '{topic.description}'}});\n"
    f.write(topic_query)
    f.close()

def relationship_cypher_query(relationship):
    f = open("../backend/resources/gemini_data.txt", "w+")
    f.write(f"MATCH (n1:Source {{id: '{relationship.source}'}}), (n2:Target {{id: '{relationship.target}'}}) CREATE (n1)-[:'{relationship.label}']->(n2);\n")  # edge
    f.close()

def paper_cypher_query(paper):
    f = open("../backend/resources/gemini_data.txt", "w+")
    paper_query = f"CREATE (n:Paper {{ id: '{paper.name}', arxiv_id: '{paper.arxiv_id}', url: '{paper.url}', citation_count: '{paper.citation_count}', title: '{paper.title}', abstract: '{paper.abstract}', authors: '{paper.authors}', publication_date: '{paper.publication_date}', references: '{paper.references}'}});\n"
    f.write(paper_query)  # edge
    f.close()


# TODO: File open and close issue

# ======================== CHECKS FOR MAIN FUNCTION ========================

# check if the topic name is unique
# check if the format is in json
# check if it tallies with db_operations

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def is_repeated_topic_name(topic_name):
    db = Memgraph()
    topics = json.loads(get_topics(db))

    if any(topic['name'] == topic_name for topic in topics):
        print("The topic name is not unique")
        return True
    return False

# ======================== MAIN FUNCTION ========================

# def gemini_response_to_file(gemini_response):
#     # check if the format is in json
#     if not is_json(gemini_response):
#         print("The input is not in json format")
#         return

#     # assuming gemini_response is a json string, with an array of objects (either topics or relationships)
#     response_json = json.loads(gemini_response)

#     for topic in response_json.topics:
#         # check if the topic name is unique
#         if is_repeated_topic_name(topic.name):
#             return
        
#         # write to db
#         topic_cypher_query(topic)

#     for relationship in response_json.relationships:
#         relationship_cypher_query(relationship)
    

    

    