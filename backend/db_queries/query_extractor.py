import json
import os
import re


class QueryExtractor:
    def __init__(self):
        script_directory = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script is running
        root_directory = os.path.join(script_directory, '../..') # Define the root directory
        os.chdir(root_directory) # Change the working directory
        self.root_directory = root_directory
        self.file_path = os.path.join(self.root_directory, 'backend', 'db_queries', 'dev_data.txt')
    
    def extract_papers_from_queries(self):
         # Pattern to extract id, title, and summary from the cypher command
        pattern = r"CREATE \(n:Paper \{[^}]*id: '([^']+)',[^}]*title: '([^']+)',[^}]*abstract: '([^']+)'"

        papers = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                match = re.search(pattern, line)
                if match:
                    id, title, abstract = match.groups()
                    papers.append({'id': id, 'title': title, 'abstract': abstract})
        return papers
    
    def simplify_papers_response(self, papers):

        # Transforming the list to include only id, title, and abstract
        transformed_list = [
            {'id': f'paper_{i+1}', 'title': paper['title'], 'abstract': paper['abstract']}
            for i, paper in enumerate(papers)
        ]
        return transformed_list
    
    def get_simplified_papers(self):
        papers = self.extract_papers_from_queries()
        return self.simplify_papers_response(papers)