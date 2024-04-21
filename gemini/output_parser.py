import uuid
import json

# take in a json string of the form in data_format.json file and produce a cypher query to insert the data into the graph with a uuid

def topic_cypher_query(topic):
    topic_json = json.loads(topic)

    # generate unique id for the topic
    topic_json.id = uuid.uuid4()

    # write cypher query to file (topic node and relationships)
    f = open("../backend/resources/gemini_data.txt", "w+")
    topic_query = f"CREATE (n:Node {{ id: '{topic_json.name}', name: '{topic_json.name}', description: '{topic_json.description}'}});\n"
    f.write(topic_query)

    for r in topic_json.topic_as_target:
        f.write(f"MATCH (n1:Source {{id: '{r.id}'}}), (n2:Target {{id: '{topic_json.id}'}}) CREATE (n1)-[:'{r.label}']->(n2);\n")  # edge
    f.close()

def topics_to_file(gemini_data):
    response_json = json.loads(gemini_data)

    for topic in response_json:
        topic_cypher_query(topic)
    

    

    