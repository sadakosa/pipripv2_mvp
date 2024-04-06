# this will hold the class that downloads the arxiv data, and extracts the abstracts and references from downloaded pdfs

import requests
from bs4 import BeautifulSoup
import arxiv
import pdfplumber
import re

class ArxivDataExtractor:
    def __init__(self, paper_id):
        self.paper_id = paper_id

    def get_paper_abstract_from_web(paper_id):
        # Define the base URL for the arXiv paper
        base_url = 'http://arxiv.org/abs/'
        # Construct the full URL with the paper ID
        url = base_url + paper_id
        # Send a GET request to the arXiv paper
        response = requests.get(url)
        print("Response status code:", response.status_code)
        # Parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the abstract element within the HTML structure
        abstract = soup.find('blockquote', {'class': 'abstract mathjax'})   
        # Extract the text content of the abstract element
        abstract_text = abstract.text
        # Return the abstract text
        return abstract_text
    
    def download_pdf(paper_id):
        # Define the base URL for the arXiv paper
        paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
        # Download the PDF to the PWD with a default filename.
        paper.download_pdf(dirpath="./papers_cache", filename=paper_id+".pdf")
    
    def extract_references_from_pdf(pdf_path):
        references_started = False
        collected_text = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Check if we've reached the References section
                    if 'References' in text or references_started:
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