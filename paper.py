import json
from datetime import datetime

from arxiv_utils import extract_references_from_pdf, find_arxiv_ids_in_text, search_papers_by_arxiv_id


class Paper:
    def __init__(self, arxiv_result):
        self.paper_id = arxiv_result.pdf_url.split('/')[-1]
        self.title = arxiv_result.title
        self.abstract = arxiv_result.summary
        self.authors = [a.name for a in arxiv_result.authors]
        self.publication_date = arxiv_result.published
        self.last_updated = arxiv_result.updated
        self.references = []  # list of Paper objects which this paper cites

    # Alternative constructor to instantiate the Paper using a json, for avoiding repeated API calls
    # Usage: paper = Paper.from_json("papers_cache/paper_id.json")
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

    # Manually parse references from downloaded pdf (slow and might be inaccurate depending on citation style)
    # If the references contain arxiv IDs, batch the IDs and send arxiv request to flesh out contents
    def populateReferencesUsingPdf(self, pdf_path):
        references_block = extract_references_from_pdf(pdf_path)
        arxiv_ids = find_arxiv_ids_in_text(references_block)
        results = search_papers_by_arxiv_id(arxiv_ids, download=False)
        for res in results:
            referenced_paper = Paper(res)
            self.references.append(referenced_paper)

    # Search for the article on Google Scholar and populate references if found
    # Unfortunately the payload does not contain full abstracts of the papers
    # If the resource contains an arxiv paper ID, more metadata can be retrieved from arxiv
    def populateReferencesUsingGoogleScholar(self):
        pass

    # Dev only: Writes out DB queries to convert the paper and references to nodes
    # Citation edges are generated for the paper node and its reference nodes
    # TODO: handle special characters like ' from strings as they result in invalid queries
    def writeCypherQueries(self):
        # self.references = [Paper.from_json("papers_cache/2404.00459v1.json")]
        f = open("resources/dev_data.txt", "w+")
        main_paper_query = f"CREATE (n:Node {{ id: '{self.paper_id}', title: '{self.title}', authors: {self.authors}, publication_date: '{self.publication_date}'}});\n"
        f.write(main_paper_query)
        for r in self.references:
            f.write(f"CREATE (n:Node {{ id: '{r.paper_id}', title: '{r.title}', authors: {r.authors}, publication_date: '{r.publication_date}'}});\n")
            f.write(f"MATCH (n1:Node {{id: '{r.paper_id}'}}), (n2:Node {{id: '{self.paper_id}'}}) CREATE (n1)-[:is_cited_by]->(n2);\n")  # edge
        f.close()
