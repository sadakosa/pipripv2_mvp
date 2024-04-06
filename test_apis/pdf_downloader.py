# using https://github.com/lukasschwab/arxiv.py to download pdfs from arxiv given the arxiv id

import arxiv

def download_pdf(paper_id):
    paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
    paper.download_pdf(dirpath="./papers_cache", filename="downloaded-paper.pdf")

if __name__ == '__main__':
    paper_id = '2404.00459'
    pdf_url = download_pdf(paper_id)
