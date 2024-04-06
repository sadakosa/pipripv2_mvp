# pull together the abstract extractor, and pdf downloader and references extractor to get the abstracts and retreive any cited arxiv files with 1 depth length.id

from arxiv_api import ArxivDataExtractor

def get_abstracts_iteratively(paper_id):
    # Download the PDF
    ArxivDataExtractor.download_pdf(paper_id)
    # Extract references from the PDF
    references_text = ArxivDataExtractor.extract_references_from_pdf("./papers_cache/"+paper_id+".pdf")
    # Find arXiv IDs within the references text
    arxiv_ids = ArxivDataExtractor.find_arxiv_ids_in_text(references_text)
    arxiv_ids.append(paper_id)
    # Get the abstracts of the cited papers
    for arxiv_id in arxiv_ids:
        abstract = ArxivDataExtractor.get_paper_abstract_from_web(arxiv_id)

def main():
    get_abstracts_iteratively("2404.00459")

if __name__ == "__main__":
    main()