import json
import os

from backend.api_utils.arxiv_utils import search_papers_by_arxiv_id
from backend.api_utils.semantic_scholar_utils import get_references, get_citations
from backend.pdf_parsers import extract_references_from_pdf, find_arxiv_ids_in_text


class Paper:
    def __init__(self, ss_data):
        self.paper_id = ss_data.get("paperId")
        self.arxiv_id = ss_data.get("externalIds", dict()).get('ArXiv', "")
        self.url = ss_data.get("url", "")
        self.title = ss_data.get("title", "")
        self.abstract = ss_data.get("abstract", "")
        self.authors = [a.get("name", "") for a in ss_data.get("authors")]
        self.publication_date = ss_data.get("publicationDate", "")
        if self.publication_date is None:
            self.publication_date = ""
        self.last_updated = self.publication_date
        self.references = []  # list of Paper objects which this paper cites
        self.citations = []  # list of Paper objects which cite this paper
        self.citation_count = ss_data.get("citationCount", -1)

    @classmethod
    def from_arxiv(cls, arxiv_response):
        paper_obj = cls.__new__(cls)
        super(Paper, paper_obj).__init__() # call any polymorphic base class initializers

        paper_obj.arxiv_id = arxiv_response.pdf_url.split('/')[-1]
        paper_obj.paper_id = "arxiv-" + paper_obj.arxiv_id
        paper_obj.url = arxiv_response.pdf_url
        paper_obj.title = arxiv_response.title
        paper_obj.abstract = arxiv_response.summary
        paper_obj.authors = [a.name for a in arxiv_response.authors]
        paper_obj.publication_date = arxiv_response.published.isoformat()
        paper_obj.last_updated = arxiv_response.updated.isoformat()
        paper_obj.references = []  # list of Paper objects which this paper cites
        paper_obj.citations = []  # list of Paper objects which cite this paper
        paper_obj.citation_count = -1

        return paper_obj

    # Alternative constructor to instantiate the Paper using a json, for avoiding repeated API calls
    # Usage: paper = Paper.from_json("papers_cache/paper_id.json")
    @classmethod
    def from_json(cls, json_path):
        with open(json_path, 'r') as json_file:
            paper_metadata = json.load(json_file)

        paper_obj = cls.__new__(cls)
        super(Paper, paper_obj).__init__()
        paper_obj.arxiv_id = paper_metadata.get("arxiv_id")
        paper_obj.paper_id = paper_metadata.get("paper_id")
        paper_obj.url = paper_metadata.get("url")
        paper_obj.title = paper_metadata.get("title")
        paper_obj.abstract = paper_metadata.get("abstract")
        paper_obj.authors = paper_metadata.get("authors")
        paper_obj.publication_date = paper_metadata.get("publication_date")
        paper_obj.last_updated = paper_metadata.get("last_updated")
        paper_obj.references = paper_metadata.get("references")
        paper_obj.citations = paper_metadata.get("citations")
        paper_obj.citation_count = paper_metadata.get("citation_count")

        return paper_obj

    def to_json(self, references=[], citations=[]):
        return {
            "paper_id": self.paper_id,
            "arxiv_id": self.arxiv_id,
            "url": self.url,
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "publication_date": self.publication_date,
            "last_updated": self.last_updated,
            "references": [ref.to_json() for ref in references],  # at most one level to prevent infinite loop
            "citations": [c.to_json() for c in citations],
            "citation_count": self.citation_count
        }

    # Exports the paper metadata in json format
    def save_as_json(self, save_directory="papers_cache"):
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        paper_metadata = self.to_json(self.references, self.citations)

        file_path = f"{save_directory}/{self.paper_id}.json"
        with open(file_path, 'w') as json_file:
            json.dump(paper_metadata, json_file, indent=2)
            print(f"Saved {file_path}.")

    # Populate references using Semantic Scholar references endpoint
    # Only works for papers which have a SS ID
    def populateReferencesUsingSS(self):
        references = get_references(self.paper_id)
        for ref in references:
            referenced_paper = Paper(ref.get("citedPaper"))
            self.references.append(referenced_paper)

    def populateCitationsUsingSS(self):
        citations = get_citations(self.paper_id)
        for c in citations:
            citing_paper = Paper(c.get("citingPaper"))
            self.citations.append(citing_paper)

    # Manually parse references from downloaded pdf (slow and might be inaccurate depending on citation style)
    # If the references contain arxiv IDs, batch the IDs and send arxiv request to flesh out contents
    def populateReferencesUsingPdf(self, pdf_path):
        references_block = extract_references_from_pdf(pdf_path)
        arxiv_ids = find_arxiv_ids_in_text(references_block)
        results = search_papers_by_arxiv_id(arxiv_ids)
        for res in results:
            referenced_paper = Paper.from_arxiv(res)
            self.references.append(referenced_paper)

    # Dev only: Writes out DB queries to convert the paper and references to nodes
    # Citation edges are generated for the paper node and its reference nodes
    # TODO: handle special characters like ' from strings as they result in invalid queries
    def writeCypherQueries(self):
        # self.references = [Paper.from_json("papers_cache/2404.00459v1.json")]
        f = open("backend/resources/dev_data.txt", "w+")
        main_paper_query = f"CREATE (n:Node {{ id: '{self.paper_id}', title: '{self.title}', authors: {self.authors}, publication_date: '{self.publication_date}'}});\n"
        f.write(main_paper_query)

        for r in self.references:
            f.write(f"CREATE (n:Node {{ id: '{r.paper_id}', title: '{r.title}', authors: {r.authors}, publication_date: '{r.publication_date}'}});\n")
            f.write(f"MATCH (n1:Node {{id: '{r.paper_id}'}}), (n2:Node {{id: '{self.paper_id}'}}) CREATE (n1)-[:is_cited_by]->(n2);\n")  # edge
        f.close()
