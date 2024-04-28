# Utils for downloading the arxiv data, and extracting abstracts and references from downloaded pdfs

import requests
from arxiv import Search, Client
# from bs4 import BeautifulSoup
import os


# def get_paper_abstract_from_web(paper_id):
#     # Define the base URL for the arXiv paper
#     base_url = 'http://arxiv.org/abs/'
#     url = base_url + paper_id
#
#     # Send a GET request to the arXiv paper & the abstract element within the HTML structure
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     abstract = soup.find('blockquote', {'class': 'abstract mathjax'})
#     abstract_text = abstract.text
#
#     return abstract_text


def search_papers_by_arxiv_id(paper_ids):
    arxiv_client = Client()
    results = arxiv_client.results(Search(id_list=paper_ids))
    return results


def download_from_arxiv_response(arxiv_response, save_directory="papers_cache"):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for res in arxiv_response:
        pdf_url = res.pdf_url
        if pdf_url:
            paper_id = pdf_url.split('/')[-1]  # Extract paper ID from URL
            res.download_pdf(dirpath=save_directory, filename=paper_id + ".pdf")
            print(f"Downloaded {res.title} as {save_directory}/{paper_id}.pdf")
