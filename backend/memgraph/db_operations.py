import json


def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    print("clearing database")
    db.execute_query(command)


def populate_database(db, path):
    with open(path, 'r', encoding='windows-1252') as file:  # Adjust the encoding if necessary
        lines = file.readlines()
    # file = open(path)
    # lines = file.readlines()
    file.close()
    for line in lines:
        if len(line.strip()) != 0 and line[0] != '/':
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
        data = {
            "id": n.properties.get('id', 'No ID'),
            "description": n.properties.get('description', 'No Description')
            }
        node_objects.append(data)

    for paper in papers:
        n = paper['n']
        data = {
            "type": "Paper", 
            "id": n.id, 
            "arxiv_id": n.properties.get('arxiv_id', 'N/A'),
            "url": n.properties.get('url', 'N/A'),
            "citation_count": n.properties.get('citation_count', 'N/A'),
            "title": n.properties.get('title', 'No Title'),
            "abstract": n.properties.get('abstract', 'No Abstract'),
            "authors": json.dumps(n.properties.get('authors', [])),
            "publication_date": n.properties.get('publication_date', 'No Date'),
            "references": json.dumps(n.properties.get('references', []))
            }
        node_objects.append(data)

    return json.dumps(node_objects)

def get_topics(db):
    command = "MATCH (n:Topic) RETURN n;"
    topics = db.execute_and_fetch(command)

    node_objects = []
    for topic in topics:
        n = topic['n']
        data = {
            "id": n.properties['id'],
            "description": n.properties['description']
            }
    return json.dumps(node_objects)

def get_relationships(db):
    try:
        command = "MATCH (n1)-[r]-(n2) RETURN n1, r, n2;"
        relationships = db.execute_and_fetch(command)

        relationship_objects = []
        for relationship in relationships:
            source = relationship.get('source', 'No Source')
            target = relationship.get('target', 'No Target')

            data = {"source": source.properties.get('name', 'no name'),
                    "target": target.properties.get('name', 'no name')}
            relationship_objects.append(data)

        return json.dumps(relationship_objects)
    except Exception as e:
        print(f"Error retrieving relationships: {str(e)}")
        return []


def paper_or_topic(node):
    if 'authors' in node.properties:
        # data = {"type": "paper", "id": node.properties['id'], "name": node.properties['name'], "author": node.properties['author'], "title": node.properties['title'], "summary": node.properties['summary']}
        data = {
            "type": "Paper", 
            "id": node.id, 
            "arxiv_id": node.properties.get('arxiv_id', 'N/A'),
            "url": node.properties.get('url', 'N/A'),
            "citation_count": node.properties.get('citation_count', 'N/A'),
            "title": node.properties.get('title', 'No Title'),
            "abstract": node.properties.get('abstract', 'No Abstract'),
            "authors": json.dumps(node.properties.get('authors', [])),
            "publication_date": node.properties.get('publication_date', 'No Date'),
            "references": json.dumps(node.properties.get('references', []))
            }
        return data
    else:
        # data = {"type": "topic", "id": node.properties['id'], "name": node.properties['name'], "summary": node.properties['summary']}
        print("Node with ID {} is considered a topic.".format(node.id))
        data = {
            "type": "Topic", 
            # "id": node.id, # name of topic
            "id": node.properties.get('id', 'No Topic Name'),
            "description": node.properties.get('description', 'No description available')
            }
        return data

def get_graph(db):
    command = "MATCH (n1)-[r]-(n2) RETURN n1, labels(n1) AS n1_labels, type(r) AS label, r, n2, labels(n2) AS n2_labels;"
    relationships = db.execute_and_fetch(command)
    print("in get_graph")

    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        r = relationship['r']
        # print(r)
        data = {
            "source": r.nodes[0], 
            "target": r.nodes[1], 
            "label": relationship['label']
            }
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

    data = {"links": link_objects, "nodes": node_objects}

    return json.dumps(data)
