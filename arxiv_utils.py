# Utils for downloading the arxiv data, and extracting abstracts and references from downloaded pdfs

import requests
from arxiv import Search, Client
from bs4 import BeautifulSoup
import pdfplumber
import re
import os

from paper import Paper


def get_paper_abstract_from_web(paper_id):
    # Define the base URL for the arXiv paper
    base_url = 'http://arxiv.org/abs/'
    url = base_url + paper_id

    # Send a GET request to the arXiv paper & the abstract element within the HTML structure
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    abstract = soup.find('blockquote', {'class': 'abstract mathjax'})
    abstract_text = abstract.text

    return abstract_text

def load_papers_from_arxiv(paper_ids, save_directory="papers_cache", download=True):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    arxiv_client = Client()

    papers = []
    results = arxiv_client.results(Search(id_list=paper_ids))
    for res in results:
        pdf_url = res.pdf_url
        if pdf_url and download:
            paper_id = pdf_url.split('/')[-1]  # Extract paper ID from URL
            res.download_pdf(dirpath=save_directory, filename=paper_id + ".pdf")
            print(f"Downloaded {res.title} as {save_directory}/{paper_id}.pdf")
        paper = Paper(res)
        papers.append(paper)
    return papers

def extract_references_from_pdf(pdf_path):
    references_started = False
    collected_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Check if we've reached the References section
                if 'References' in text or 'REFERENCES' in text or references_started:
                    references_started = True
                    collected_text.append(text)

    # Join all collected text
    full_text = "\n".join(collected_text)
    return full_text

def find_arxiv_ids_in_text(text):
    # Simple regex to find arXiv IDs; might need refinement based on actual reference formats
    array_of_ids = re.findall(r'arXiv:\d+\.\d+', text)
    cleaned_array = []

    for element in array_of_ids:
        cleaned_array.append(element.replace("arXiv:", ""))

    return cleaned_array