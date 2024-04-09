import json
from datetime import datetime


class Paper:
    def __init__(self, arxiv_result):
        self.paper_id = arxiv_result.pdf_url.split('/')[-1]
        self.title = arxiv_result.title
        self.abstract = arxiv_result.summary
        self.authors = [a.name for a in arxiv_result.authors]
        self.publication_date = arxiv_result.published
        self.last_updated = arxiv_result.updated
        self.references = []

    # Alternative constructor to instantiate the Paper using a json, for avoiding repeated API calls
    # Usage: paper = Paper.from_json("file_name.json")
    @classmethod
    def from_json(cls, json_path):
        with open(json_path, 'r') as json_file:
            paper_metadata = json.load(json_file)

        paper_obj = cls.__new__(cls)
        super(Paper, paper_obj).__init__() # call any polymorphic base class initializers
        paper_obj.paper_id = paper_metadata.get("paper_id")
        paper_obj.title = paper_metadata.get("title")
        paper_obj.abstract = paper_metadata.get("abstract")
        paper_obj.authors = paper_metadata.get("authors")
        paper_obj.publication_date = datetime.fromisoformat(paper_metadata.get("publication_date"))
        paper_obj.last_updated = datetime.fromisoformat(paper_metadata.get("last_updated"))
        paper_obj.references = paper_metadata.get("references")

        return paper_obj

    # Exports the paper metadata in json format
    def save_as_json(self, save_directory="papers_cache"):
        paper_metadata = {
            "paper_id": self.paper_id,
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "publication_date": self.publication_date.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "references": self.references
        }

        file_path = f"{save_directory}/{self.paper_id}.json"
        with open(file_path, 'w') as json_file:
            json.dump(paper_metadata, json_file, indent=4)
            print(f"Saved {file_path}.")
