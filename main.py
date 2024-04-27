from backend.api_utils.semantic_scholar_utils import search_papers_by_id
from backend.gemini.gemini_client import GeminiClient
from backend.graph import Graph
from backend.memgraph.query_generator import generate_queries_for_graph, write_queries_to_txt_file
from backend.paper import Paper


def main():
    seed_ids = ["2404.00459"]#, "2304.03442"]
    papers = []
    response = search_papers_by_id(arxiv_ids=seed_ids)
    for r in response:
        paper = Paper(r)
        paper.populateReferencesUsingSS()
        papers.append(paper)
    # for path in ["papers_cache/5278a8eb2ba2429d4029745caf4e661080073c81.json"]:#, "papers_cache/b9750286ba2198a406137e0dfee2d545f0d78c13.json"]:
    #     paper = Paper.from_json(path)
    #     print(paper)

    gem = GeminiClient()
    referenced_papers = []
    for paper in papers:
        referenced_papers += paper.references
    l2_topics, l2_edges = gem.generate_l2_topics_and_edges(papers + referenced_papers)
    l1_topics, l1_edges = gem.generate_l1_topics_and_edges(l2_topics)
    graph = Graph(topics=l2_topics + l1_topics, edges=l2_edges + l1_edges, papers=papers)

    queries = generate_queries_for_graph(graph)
    print(queries[0], queries[1])
    write_queries_to_txt_file(queries)
    print("end")


if __name__ == "__main__":
    main()
