import pdfplumber
import re

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