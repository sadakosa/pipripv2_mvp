from backend.api_utils.semantic_scholar_utils import search_papers_by_id
from backend.paper import Paper
from backend.topic import Topic
from backend.gemini import initialise_model, start_chat, get_chat_response

def main():
    papers = []
    #results = search_papers_by_arxiv_id(["2404.00459", "2304.03442"], download=False)
    #refs = extract_references_from_pdf("./papers_cache/2304.03442v2.pdf")
    #arxiv_ids = find_arxiv_ids_in_text(refs)

    #response = search_papers_by_id(arxiv_ids=["2404.00459", "2304.03442"])
    #for r in response:
    #     paper = Paper(r)
    #     paper.populateReferencesUsingSS()
    #     papers.append(paper)
    #     paper.save_as_json()
    #for path in ["papers_cache/5278a8eb2ba2429d4029745caf4e661080073c81.json"]:#, "papers_cache/b9750286ba2198a406137e0dfee2d545f0d78c13.json"]:
    #    paper = Paper.from_json(path)
    #    print(paper)
    #    paper.writeCypherQueries()
    model = initialise_model()
    chat = start_chat(model)
    #response = get_chat_response(chat, "[STEP 1]" + "[ABSTRACT] 1" + paper1.abstract + "[ABSTRACT] 2"+ paper2.abstract)

if __name__ == "__main__":
    main()
