# using https://github.com/lukasschwab/arxiv.py to download pdfs from arxiv given the arxiv id

import arxiv

def download_pdf(paper_id):
    # Define the base URL for the arXiv paper
    paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
    # Download the PDF to the PWD with a default filename.
    # paper.download_pdf()
    # Download the PDF to the PWD with a custom filename.
    # paper.download_pdf(filename="downloaded-paper.pdf")
    # Download the PDF to a specified directory with a custom filename.
    paper.download_pdf(dirpath="./papers_cache", filename="downloaded-paper.pdf")

if __name__ == '__main__':
    paper_id = '2404.00459'
    pdf_url = download_pdf(paper_id)
    print(pdf_url)
# Path: pdf_downloader.py