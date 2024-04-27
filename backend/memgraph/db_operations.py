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
        data = {
            "id": n.properties['id'],
            "description": n.properties['description']
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
            "type": "paper",
            "id": node.id,
            "arxiv_id": node.properties['arxiv_id'],
            "url": node.properties['url'],
            "citation_count": node.properties['citation_count'],
            "title": node.properties['title'],
            "abstract": node.properties['abstract'],
            "authors": node.properties['authors'],
            "publication_date": node.properties['publication_date']
            # "references": json.dump(node.properties['references'])
        }
        return data
    else:
        # data = {"type": "topic", "id": node.properties['id'], "name": node.properties['name'], "summary": node.properties['summary']}
        data = {
            "type": "topic",
            "id": node.id,  # name of topic
            "description": node.properties['description']
        }
        return data


def get_graph(db):
    command = "MATCH (n1)-[r]-(n2) RETURN n1, labels(n1) AS n1_labels, type(r) AS label, r, n2, labels(n2) AS n2_labels;"
    relationships = db.execute_and_fetch(command)
    print("in get_graph")

    link_objects = []
    # command = "MATCH (n:Paper) RETURN n;"
    # papers = db.execute_and_fetch(command)
    # command = "MATCH (n:Topic) RETURN n;"
    # topics = db.execute_and_fetch(command)
    node_objects = []
    added_nodes = []
    # for node in papers:
    #     n = node['n']
    #     if not (n.id in added_nodes):
    #         data = paper_or_topic(n)
    #         node_objects.append(data)
    #         added_nodes.append(n.id)
    # for node in topics:
    #     n = node['n']
    #     if not (n.id in added_nodes):
    #         data = paper_or_topic(n)
    #         node_objects.append(data)
    #         added_nodes.append(n.id)
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
