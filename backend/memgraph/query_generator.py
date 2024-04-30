# from backend.memgraph.database.memgraph import Memgraph
from backend.edge import Edge
from backend.memgraph.db_utils import cleanse
from backend.graph import Graph
from backend.paper import Paper
from backend.topic import Topic


def generate_topic_queries(topics: list[Topic]):
    queries = []
    for topic in topics:
        q = f"CREATE (n:Topic {{ id: '{cleanse(topic.id)}', description: '{cleanse(topic.description)}'}});\n"
        queries.append(q)
    return queries


def generate_edge_queries(edges: list[Edge]):
    queries = []
    for edge in edges:
        q = f"MATCH (n1:{edge.source_type} {{id: '{cleanse(edge.source)}'}}), (n2:{edge.target_type} {{id: '{cleanse(edge.target)}'}}) CREATE (n1)-[:{edge.label}]->(n2);\n"
        queries.append(q)
    return queries


def generate_paper_queries(papers: list[Paper]):
    queries = []
    for paper in papers:
        paper_query = f"CREATE (n:Paper {{ id: '{paper.paper_id}', arxiv_id: '{paper.arxiv_id}', url: '{paper.url}', citation_count: '{paper.citation_count}', title: '{cleanse(paper.title)}', abstract: '{cleanse(paper.abstract)}', authors: {[cleanse(a) for a in paper.authors]}, publication_date: '{paper.publication_date}'}});\n"
        queries.append(paper_query)
        queries += generate_paper_queries(paper.references)
        queries += generate_paper_queries(paper.citations)
    return queries


def generate_queries_for_graph(g: Graph):
    queries = generate_topic_queries(g.topics) + generate_paper_queries(g.papers) + generate_edge_queries(g.edges)
    return queries


# dev only
def write_queries_to_txt_file(queries, path="backend/resources/dev_data.txt"):
    f = open(path, "w+")
    for query in queries:
        f.write(query)
    f.close()
