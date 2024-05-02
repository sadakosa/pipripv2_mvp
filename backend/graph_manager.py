from backend.api_utils.arxiv_utils import search_papers_by_arxiv_id
from backend.api_utils.semantic_scholar_utils import search_papers_by_id
from backend.edge import Edge
from backend.gemini.gemini_client import GeminiClient
from backend.graph import Graph
from backend.paper import Paper


# Remove the edge if there is an existing reversed edge
def removeDuplicateEdges(edges: list[Edge]):
    existing_edges = {}
    final_edges = []
    for edge in edges:
        key1 = edge.source + "-" + edge.target
        key2 = edge.target + "-" + edge.source
        if key1 in existing_edges or key2 in existing_edges:
            print("Discarding edge " + key1)
            continue
        existing_edges[key1] = True
        final_edges.append(edge)
    return final_edges


def build_graph_from_paper_ids(arxiv_ids=[], ss_ids=[], get_citations=False, get_references=False, existing_l2_topics=[]):
    papers = []
    response = search_papers_by_id(arxiv_ids=arxiv_ids, ss_ids=ss_ids)
    if response:
        for r in response:
            paper = Paper(r)
            if get_references:
                paper.populateReferencesUsingSS()
            if get_citations:
                paper.populateCitationsUsingSS()
            papers.append(paper)
    else:  # if rate limited, fall back to arxiv API if arxiv ID is available
        arxiv_response = search_papers_by_arxiv_id(arxiv_ids)
        for r in arxiv_response:
            paper = Paper.from_arxiv(r)
            papers.append(paper)
        print(f"Rate limited, collected {len(papers)} papers from Arxiv API instead.")
    if not papers:
        return None  # None of the APIs returned anything

    gem = GeminiClient()
    referenced_papers = []
    reference_edges = []
    citing_papers = []
    citation_edges = []
    for paper in papers:
        referenced_papers += paper.references
        for ref in paper.references:
            edge = Edge({
                "source_type": "Paper",
                "target_type": "Paper",
                "source": ref.paper_id,
                "target": paper.paper_id,
                "label": "cited_by"
            })
            reference_edges.append(edge)
    for paper in papers:
        citing_papers += paper.citations
        for c in paper.citations:
            edge = Edge({
                "source_type": "Paper",
                "target_type": "Paper",
                "source": paper.paper_id,
                "target": c.paper_id,
                "label": "cited_by"
            })
            citation_edges.append(edge)
    l2_topics, l2_edges = gem.generate_l2_topics_and_edges(papers + referenced_papers + citing_papers)
    l1_topics, l1_edges = gem.generate_l1_topics_and_edges(l2_topics + existing_l2_topics)
    l1_topic_edges = gem.generate_topic_topic_edges(l1_topics)
    # Remove the duplicate edges first
    final_edges = removeDuplicateEdges(l2_edges + l1_edges + reference_edges + citation_edges + l1_topic_edges)
    graph = Graph(l1_topics=l1_topics, l2_topics=l2_topics, edges=final_edges, papers=papers)
    # graph = Graph(l1_topics=l1_topics, l2_topics=l2_topics, edges=l2_edges + l1_edges + reference_edges + citation_edges + l1_topic_edges, papers=papers)
    print(f"Generated graph with {len(graph.l1_topics)} L1 topics, {len(graph.l2_topics)} L2 topics, {len(graph.edges)} edges and {len(graph.papers)} root papers.")

    return graph
