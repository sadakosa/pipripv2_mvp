import json


def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)


def populate_database(db, path):
    file = open(path)
    lines = file.readlines()
    file.close()
    for line in lines:
        if len(line.strip()) != 0 and line[0] != '/':
            db.execute_query(line)

# Execute Cypher query to link papers which share at least one common author
# def generate_shared_author_edges(db):
#     pass

def get_nodes(db):
    command = "MATCH (n:Node) RETURN n;"
    nodes = db.execute_and_fetch(command)

    node_objects = []
    for node in nodes:
        n = node['n']
        data = {"id": n.properties['id'], "name": n.properties['title']}
        node_objects.append(data)

    return json.dumps(node_objects)


def get_relationships(db):
    command = "MATCH (n1)-[e:is_cited_by]-(n2) RETURN n1,n2,e;"
    relationships = db.execute_and_fetch(command)

    relationship_objects = []
    for relationship in relationships:
        n1 = relationship['n1']
        n2 = relationship['n2']

        data = {"userOne": n1.properties['title'],
                "userTwo": n2.properties['title']}
        relationship_objects.append(data)

    return json.dumps(relationship_objects)


def get_graph(db):
    command = "MATCH (n1)-[e:is_cited_by]-(n2) RETURN n1,n2,e;"
    relationships = db.execute_and_fetch(command)

    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        e = relationship['e']
        data = {"source": e.nodes[0], "target": e.nodes[1]}
        link_objects.append(data)

        n1 = relationship['n1']
        if not (n1.id in added_nodes):
            data = {"id": n1.id, "name": n1.properties['title']}
            node_objects.append(data)
            added_nodes.append(n1.id)

        n2 = relationship['n2']
        if not (n2.id in added_nodes):
            data = {"id": n2.id, "name": n2.properties['title']}
            node_objects.append(data)
            added_nodes.append(n2.id)
    data = {"links": link_objects, "nodes": node_objects}

    return json.dumps(data)
