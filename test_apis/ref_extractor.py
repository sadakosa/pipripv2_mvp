# get pdf file from ./papers_cache/downloaded-paper.pdf and extract text after references section

import pdfplumber
import re

def extract_references(pdf_path):
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

def find_arxiv_ids(text):
    # Simple regex to find arXiv IDs; might need refinement based on actual reference formats
    return re.findall(r'arXiv:\d+\.\d+', text)


if __name__ == '__main__':
    # Path to your PDF file
    pdf_path = "./papers_cache/downloaded-paper.pdf"

    # Extract references text
    references_text = extract_references(pdf_path)

    # Find arXiv IDs within the references text
    arxiv_ids = find_arxiv_ids(references_text)

    print("Found arXiv IDs:", arxiv_ids)