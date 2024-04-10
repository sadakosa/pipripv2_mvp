# pull together the abstract extractor, and pdf downloader and references extractor to get the abstracts and retreive any cited arxiv files with 1 depth length.id

from arxiv_utils import search_papers_by_arxiv_id, extract_references_from_pdf, find_arxiv_ids_in_text
from paper import Paper


# def get_abstracts_iteratively(paper_id):
#     ArxivDataExtractor.download_papers_as_pdf([paper_id])
#     references_text = ArxivDataExtractor.extract_references_from_pdf("./papers_cache/"+paper_id+".pdf")
#     # Find arXiv IDs within the references text
#     arxiv_ids = ArxivDataExtractor.find_arxiv_ids_in_text(references_text)
#     arxiv_ids.append(paper_id)
#
#     # Get the abstracts of the cited papers
#     for arxiv_id in arxiv_ids:
#         abstract = ArxivDataExtractor.get_paper_abstract_from_web(arxiv_id)

def main():
    # get_abstracts_iteratively("2404.00459")
    papers = []
    # results = search_papers_by_arxiv_id(["2404.00459", "2304.03442"], download=False)
    # for res in results:
    #     paper = Paper(res)
    #     papers.append(paper)
    # for p in papers:
    #     p.save_as_json()
    # for path in ["papers_cache/2304.03442v2.json", "papers_cache/2404.00459v1.json"]:
    #     paper = Paper.from_json(path)
    # refs = extract_references_from_pdf("./papers_cache/2304.03442v2.pdf")
    # arxiv_ids = find_arxiv_ids_in_text(refs)

    paper = Paper.from_json("papers_cache/2304.03442v2.json")
    # paper.populateReferencesUsingPdf("papers_cache/2304.03442v2.pdf")
    # print(paper.references)
    paper.writeCypherQueries()

if __name__ == "__main__":
    main()