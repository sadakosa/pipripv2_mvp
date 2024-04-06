# Call  http://arxiv.org/abs/0705.0123 and use beautifulsoup to extract the abstract of the paper.

import requests
from bs4 import BeautifulSoup

def get_paper_abstract(paper_id):
    # Define the base URL for the arXiv paper
    base_url = 'http://arxiv.org/abs/'
    url = base_url + paper_id

    # Send a GET request to the arXiv paper + find the abstract element within the HTML structure
    response = requests.get(url)
    print("Response status code:", response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    abstract = soup.find('blockquote', {'class': 'abstract mathjax'})   
    abstract_text = abstract.text

    return abstract_text

if __name__ == '__main__':
    paper_id = '0705.0123'
    abstract = get_paper_abstract(paper_id)
    print(abstract)