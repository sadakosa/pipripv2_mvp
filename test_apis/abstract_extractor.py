# Call  http://arxiv.org/abs/0705.0123 and use beautifulsoup to extract the abstract of the paper.

import requests
from bs4 import BeautifulSoup

def get_paper_abstract(paper_id):
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

if __name__ == '__main__':
    paper_id = '0705.0123'
    abstract = get_paper_abstract(paper_id)
    print(abstract)