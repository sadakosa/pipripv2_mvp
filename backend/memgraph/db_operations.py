import json


def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    print("clearing database")
    db.execute_query(command)


def populate_database(db, path):
    file = open(path)
    lines = file.readlines()
    file.close()
    for line in lines:
        if len(line.strip()) != 0 and line[0] != '/':
            # print(line)
            db.execute_query(line)

# Execute Cypher query to link papers which share at least one common author
# def generate_shared_author_edges(db):
#     pass

def get_nodes(db):
    command = "MATCH (n:Paper) RETURN n;"
    papers = db.execute_and_fetch(command)
    command = "MATCH (n:Topic) RETURN n;"
    topics = db.execute_and_fetch(command)

    node_objects = []
    for topic in topics:
        n = topic['n']
        data = {"id": n.properties['id'],"description": n.properties['description']}
        node_objects.append(data)

    for paper in papers:
        n = paper['n']
        data = {"id": n.properties['id'], "name": n.properties['name'], "author": n.properties['author'], "title": n.properties['title'], "summary": n.properties['summary']}
        node_objects.append(data)

    return json.dumps(node_objects)

def get_topics(db):
    command = "MATCH (n:Topic) RETURN n;"
    topics = db.execute_and_fetch(command)

    node_objects = []
    for topic in topics:
        n = topic['n']
        data = {"id": n.properties['id'],"description": n.properties['description']}
        node_objects.append(data)

    return json.dumps(node_objects)

def get_relationships(db):
    command = "MATCH (n1)-[r]-(n2) RETURN n1, r, n2;"
    relationships = db.execute_and_fetch(command)

    relationship_objects = []
    for relationship in relationships:
        n1 = relationship['n1']
        n2 = relationship['n2']

        data = {"nodeN": n1.properties['name'],
                "nodeM": n2.properties['name']}
        relationship_objects.append(data)

    return json.dumps(relationship_objects)


def paper_or_topic(node):
    if 'author' in node.properties:
        # data = {"type": "paper", "id": node.properties['id'], "name": node.properties['name'], "author": node.properties['author'], "title": node.properties['title'], "summary": node.properties['summary']}
        data = {"type": "paper", "id": node.id, "name": node.properties['name'], "author": node.properties['author'], "title": node.properties['title'], "summary": node.properties['summary']}
        return data
    else:
        # data = {"type": "topic", "id": node.properties['id'], "name": node.properties['name'], "summary": node.properties['summary']}
        data = {"type": "topic", "id": node.id, "name": node.properties['name'], "summary": node.properties['summary']}
        return data

def get_graph(db):
    command = "MATCH (n1)-[r]-(n2) RETURN n1, labels(n1) AS n1_labels, type(r) AS relationship_type, r, n2, labels(n2) AS n2_labels;"
    relationships = db.execute_and_fetch(command)
    print("in get_graph")

    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        r = relationship['r']
        # print(r)
        data = {"source": r.nodes[0], "target": r.nodes[1], "relationship_type": relationship['relationship_type']}
        link_objects.append(data)

        n1 = relationship['n1']
        if not (n1.id in added_nodes):
            data = paper_or_topic(n1)
            node_objects.append(data)
            added_nodes.append(n1.id)

        n2 = relationship['n2']
        if not (n2.id in added_nodes):
            data = paper_or_topic(n2)
            node_objects.append(data)
            added_nodes.append(n2.id)

        # old code to identify nodes by given_id and label (but changed to use neo4j db id only as shown above)
        # n1 = relationship['n1']
        # n1_label = relationship['n1_labels'][0]
        # if not (str(n1.id) + n1_label in added_nodes):
        #     data = paper_or_topic(n1, n1_label)
        #     node_objects.append(data)
        #     added_nodes.append(str(n1.id) + n1_label)

        # n2 = relationship['n2']
        # n2_label = relationship['n2_labels'][0]
        # if not (str(n2.id) + n2_label in added_nodes):
        #     data = paper_or_topic(n2, n2_label)
        #     node_objects.append(data)
        #     added_nodes.append(str(n2.id) + n2_label)

    data = {"links": link_objects, "nodes": node_objects}

    return json.dumps(data)
