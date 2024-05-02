import json

from backend.topic import Topic


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

def get_papers(db):
    command = "MATCH (n:Paper) RETURN n;"
    papers = db.execute_and_fetch(command)
    node_objects = []

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
    topics_data = db.execute_and_fetch(command)

    topics = []
    for d in topics_data:
        n = d['n']
        topic_dict = {
            "id": n.properties['id'],
            "description": n.properties['description']
        }
        topic = Topic(topic_dict)
        topics.append(topic)
    return topics


def get_l2_topics(db):
    command = "MATCH (n:TopicL2) RETURN n;"
    topics_data = db.execute_and_fetch(command)

    topics = []
    for d in topics_data:
        n = d['n']
        topic_dict = {
            "id": n.properties['id'],
            "description": n.properties['description']
        }
        topic = Topic(topic_dict)
        topics.append(topic)
    return topics


def get_topic_topic_edges(db):
    command = "MATCH (n1: Topic)-[r]-(n2: Topic) RETURN n1, labels(n1) AS n1_labels, type(r) AS label, r, n2, labels(n2) AS n2_labels;"
    edges = db.execute_and_fetch(command)

    node_objects = []
    for edge in edges:
        data = {
            "source": edge['n1'].properties['id'],
            "target": edge['n2'].properties['id'],
            "label": edge['label']
        }
        node_objects.append(data)
    return node_objects


def delete_l1_topics_and_edges(db):
    command = "MATCH (t:TopicL1) DETACH DELETE t;"
    db.execute_query(command)


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
        data = {
            "type": "paper",
            "id": node.properties['id'],
            "arxiv_id": node.properties['arxiv_id'],
            "url": node.properties['url'],
            "citation_count": node.properties['citation_count'],
            "title": node.properties['title'],
            "abstract": node.properties['abstract'],
            "authors": node.properties['authors'],
            "publication_date": node.properties['publication_date']
        }
        return data
    else:
        data = {
            "type": "topic",
            "id": node.properties['id'],  # name of topic
            "description": node.properties['description']
        }
        return data


def get_graph(db):
    command = "MATCH (n1)-[r]->(n2) RETURN n1, labels(n1) AS n1_labels, type(r) AS label, r, n2, labels(n2) AS n2_labels;"
    relationships = db.execute_and_fetch(command)
    print("Getting graph...")

    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        data = {
            "source": relationship['n1'].properties['id'],
            "target": relationship['n2'].properties['id'],
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


def get_l1_graph(db):
    command = "MATCH (n1:TopicL1)-[r]->(n2) RETURN n1, labels(n1) AS n1_labels, type(r) AS label, r, n2, labels(n2) AS n2_labels UNION MATCH (n1)-[r]->(n2:TopicL1) RETURN n1, labels(n1) AS n1_labels, type(r) AS label, r, n2, labels(n2) AS n2_labels;"
    relationships = db.execute_and_fetch(command)

    link_objects = []
    node_objects = []
    added_nodes = []

    for relationship in relationships:
        data = {
            "source": relationship['n1'].properties['id'],
            "target": relationship['n2'].properties['id'],
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
