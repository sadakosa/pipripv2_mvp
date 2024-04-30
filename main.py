from backend.graph_manager import build_graph_from_paper_ids
from backend.memgraph.query_generator import generate_queries_for_graph, write_queries_to_txt_file


def main():
    arxiv_ids = ["2304.03442"]#, "2404.00459"]
    graph = build_graph_from_paper_ids(arxiv_ids, [], True, False)

    queries = generate_queries_for_graph(graph)
    print(queries[0], queries[1])
    write_queries_to_txt_file(queries)
    print("end")


if __name__ == "__main__":
    main()
