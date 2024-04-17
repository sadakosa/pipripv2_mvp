from backend.api_utils.semantic_scholar_utils import search_papers_by_id
from backend.paper import Paper

def main():
    papers = []
    # results = search_papers_by_arxiv_id(["2404.00459", "2304.03442"], download=False)
    # refs = extract_references_from_pdf("./papers_cache/2304.03442v2.pdf")
    # arxiv_ids = find_arxiv_ids_in_text(refs)

    response = search_papers_by_id(arxiv_ids=["2404.00459", "2304.03442"])
    for r in response:
        paper = Paper(r)
        paper.populateReferencesUsingSS()
        papers.append(paper)
        paper.save_as_json()
    # for path in ["papers_cache/2304.03442v2.json", "papers_cache/2404.00459v1.json"]:
    #     paper = Paper.from_json(path)

    # paper = Paper.from_json("papers_cache/2304.03442v2.json")
    # paper.populateReferencesUsingPdf("papers_cache/2304.03442v2.pdf")
    # print(paper.references)
    # paper.writeCypherQueries()

if __name__ == "__main__":
    main()