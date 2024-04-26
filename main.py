from backend.gemini.gemini_client import GeminiClient


def main():
    papers = []
    # results = search_papers_by_arxiv_id(["2404.00459", "2304.03442"], download=False)
    # refs = extract_references_from_pdf("./papers_cache/2304.03442v2.pdf")
    # arxiv_ids = find_arxiv_ids_in_text(refs)

    # response = search_papers_by_id(arxiv_ids=["2404.00459", "2304.03442"])
    # for r in response:
    #     paper = Paper(r)
    #     paper.populateReferencesUsingSS()
    #     papers.append(paper)
    #     paper.save_as_json()
    # for path in ["papers_cache/5278a8eb2ba2429d4029745caf4e661080073c81.json"]:#, "papers_cache/b9750286ba2198a406137e0dfee2d545f0d78c13.json"]:
    #     paper = Paper.from_json(path)
    #     print(paper)
    #     paper.writeCypherQueries()
    gem = GeminiClient()
    # print(gem.generate_topics_from_abstracts())
    gem.generate_l2_topic_graph()

    '''
    Gemini output
    generate topics:
    [
      {
        "id": "Generative Agents",
        "paper_ids": ["5278a8eb2ba2429d4029745caf4e661080073c81"]
      },
      {
        "id": "Personification",
        "paper_ids": ["9379d519b8ddfa194ef6f575127451e5016e1803"]
      },
      {
        "id": "Language Models",
        "paper_ids": ["5278a8eb2ba2429d4029745caf4e661080073c81"]
      },
      {
        "id": "Human Behavior Simulation",
        "paper_ids": ["5278a8eb2ba2429d4029745caf4e661080073c81"]
      },
      {
        "id": "Natural Language Processing",
        "paper_ids": ["5278a8eb2ba2429d4029745caf4e661080073c81", "9379d519b8ddfa194ef6f575127451e5016e1803"]
      },
      {
        "id": "Anthropomorphism",
        "paper_ids": ["9379d519b8ddfa194ef6f575127451e5016e1803"]
      }
    ]
    
    summarize topics:
    [
      {
        "id": "Medicine",
        "topic_ids": ["Regenerative Medicine", "Stem Cells", "Covid-19"]
      },
      {
        "id": "Social Sciences",
        "topic_ids": ["Social Graph Visualization"]
      },
      {
        "id": "Economics",
        "topic_ids": ["Capitalism"]
      }
    ]
    '''

if __name__ == "__main__":
    main()