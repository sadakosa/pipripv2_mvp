import requests
import time


def search_papers_by_id(ss_ids=[], arxiv_ids=[]):
    paper_ids = ss_ids + ["ARXIV:" + i for i in arxiv_ids]
    fields = 'title,url,abstract,publicationDate,authors,externalIds,citationCount'
    response = requests.post(
        'https://api.semanticscholar.org/graph/v1/paper/batch',
        params={'fields': fields},
        json={"ids": paper_ids}
    )
    time.sleep(1)  # avoid hitting rate limit
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Search request failed with status code {response.status_code}: {response.text}")
        return None


def get_citations(ss_id, limit=10):
    url = f'https://api.semanticscholar.org/graph/v1/paper/{ss_id}/citations'
    query_params = {'limit': limit, 'fields': 'title,url,abstract,publicationDate,authors,externalIds,citationCount'}
    response = requests.get(url, params=query_params)
    time.sleep(1)  # avoid hitting rate limit

    if response.status_code == 200:
        return response.json().get("data")
    else:
        print(f"Citations request failed with status code {response.status_code}: {response.text}")
        return []


def get_references(ss_id, limit=10):
    url = f'https://api.semanticscholar.org/graph/v1/paper/{ss_id}/references'
    query_params = {'limit': limit, 'fields': 'title,url,abstract,publicationDate,authors,externalIds,citationCount'}
    response = requests.get(url, params=query_params)
    time.sleep(1)  # avoid hitting rate limit

    if response.status_code == 200:
        return response.json().get("data")
    else:
        print(f"References request failed with status code {response.status_code}: {response.text}")
        return []
