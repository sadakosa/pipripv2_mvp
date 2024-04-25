import json
from backend.memgraph.db_operations import get_topics
# from backend.memgraph.database.memgraph import Memgraph
from backend.memgraph.db_utils import cleanse
import os

class QueryGenerator:
    def __init__(self):
        script_directory = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script is running
        root_directory = os.path.join(script_directory, '../..') # Define the root directory
        os.chdir(root_directory) # Change the working directory
        self.root_directory = root_directory
        self.file_path = os.path.join(self.root_directory, 'backend', 'db_queries', 'dev_data.txt')
    

    # ======================== WRITING CYPHER QUERIES ========================

    # take in a json string of the form in data_format.json file and produce a cypher query to insert the data into the graph with a uuid
    def topic_cypher_query(topic, f):
        topic_query = f"CREATE (n:Topic {{ id: '{topic.name}', description: '{topic.description}'}});\n"
        f.write(topic_query)

    def relationship_cypher_query(relationship, f):
        f.write(f"MATCH (n1:Source {{id: '{relationship.source}'}}), (n2:Target {{id: '{relationship.target}'}}) CREATE (n1)-[:'{relationship.label}']->(n2);\n")  # edge

    def paper_cypher_query(paper, f):
        paper_query = f"CREATE (n:Paper {{ id: '{paper.title}', arxiv_id: '{paper.arxiv_id}', url: '{paper.url}', citation_count: '{paper.citation_count}', title: '{paper.title}', abstract: '{paper.abstract}', authors: '{paper.authors}', publication_date: '{paper.publication_date}', references: '{paper.references}'}});\n"
        f.write(paper_query)  # edge


    # take in a list of topics or relationships and produce a cypher query to insert the data into the graph with a uuid
    def list_to_cypher_query(self, data, data_type):
        f = open(self.file_path, "w+")

        if data_type == "topic":
            for topic in data:
                self.topic_cypher_query(topic, f)
        elif data_type == "relationship":
            for relationship in data:
                self.relationship_cypher_query(relationship, f)
        elif data_type == "paper":
            for paper in data:
                self.paper_cypher_query(paper, f)

        f.close()

    # Dev only: Writes out DB queries to convert the paper and references to nodes
    # Citation edges are generated for the paper node and its reference nodes
    def write_papers_from_api(self, paper_json):
        print(self.file_path)
        print("root_directory: ", self.root_directory)
        f = open(self.file_path, "w+")

        main_paper_query = f"CREATE (n:Paper {{ id: '{paper_json.paper_id}', title: '{cleanse(paper_json.title)}', name: '{cleanse(paper_json.title)}', author: {[cleanse(a) for a in paper_json.authors]}, summary: '{cleanse(paper_json.abstract)}', publication_date: '{paper_json.publication_date}'}});\n"
        f.write(main_paper_query)
        print("main_paper_query: ", main_paper_query)

        for r in paper_json.references:
            f.write(f"CREATE (n:Paper {{ id: '{r.paper_id}', title: '{cleanse(r.title)}', name: '{cleanse(r.title)}', author: {[cleanse(a) for a in r.authors]}, summary: '{cleanse(r.abstract)}', publication_date: '{r.publication_date}'}});\n")
            f.write(f"MATCH (n1:Paper {{id: '{r.paper_id}'}}), (n2:Paper {{id: '{paper_json.paper_id}'}}) CREATE (n1)-[:is_cited_by]->(n2);\n")  # edge
        f.close()




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

# def is_repeated_topic_name(topic_name):
#     db = Memgraph()
#     topics = json.loads(get_topics(db))

#     if any(topic['name'] == topic_name for topic in topics):
#         print("The topic name is not unique")
#         return True
#     return False

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
    

    

    