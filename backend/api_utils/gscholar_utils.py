from serpapi import GoogleSearch

# search parameters
params = {
    "api_key": "",
    "engine": "google_scholar",
    "hl": "en",
    "q": "Generative Agents"
}

search = GoogleSearch(params)
results = search.get_dict()
organic_results = results["organic_results"]
