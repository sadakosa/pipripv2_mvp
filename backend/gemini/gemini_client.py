# Gemini client that connects to Google Gemini

import google.generativeai as genai
from google.generativeai.types import content_types as ct

import json

from backend.global_methods import load_yaml_config, read_txt
from backend.topic import Topic

from backend.db_queries.query_extractor import QueryExtractor

class GeminiClient:
    def __init__(self):
        # load the prompts
        self.prompts_path = 'backend/gemini/prompts'
        self.starter_sys_prompt = read_txt(f"{self.prompts_path}/starter.txt")

        # load the api key
        config = load_yaml_config('backend/gemini/config/api_key.yaml')
        api_key = config['GEMINI_API_KEY']
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel('gemini-pro')

    # to deal with the fact that there is no system prompt in the gemini api, we will just use the starting user prompt as the system prompt
    # link: https://www.reddit.com/r/Bard/comments/1b90i8o/does_gemini_have_a_system_prompt_option_while/
    # link: https://www.googlecloudcommunity.com/gc/AI-ML/Gemini-Pro-Context-Option/m-p/684704/highlight/true#M4159
    def send_starter_system_prompt(self):
        response = self.client.generate_content(self.starter_sys_prompt)
        print(response.text)
        return response

    def send_single_prompt(self, prompt):
        response = self.client.generate_content(prompt)
        print(response.text)
        return response

    def generate_topics_from_abstracts(self):
        generate_topics_prompt = read_txt(f"{self.prompts_path}/generate_topics_smc.txt")

        query_extractor = QueryExtractor()
        paper_abstracts = query_extractor.get_simplified_paper_abstracts()
        # test_abstracts = read_txt(f"{self.prompts_path}/sample_abstracts.txt")  # TODO: replace with actual DB query
        serialized_data = json.dumps(paper_abstracts) # Serialize your data to a JSON string
        # papers_blob = ct.to_blob(serialized_data) # Assuming the `to_blob` method can accept a string and convert it to a Blob

        response_one = self.send_single_prompt([generate_topics_prompt])
        print("response_one:", response_one.text)
        response_two = self.send_single_prompt([serialized_data])
        print("response_two:", response_two.text)

        topics = []
        edges = []  # TODO: populate edges
        try:
            json_array = json.loads(response_two.text)
            for d in json_array:
                topic = Topic(d)
                topics.append(topic)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        return topics

    def summarize_topics(self):
        summarize_topics_prompt = read_txt(f"{self.prompts_path}/summarize_topics.txt")
        test_topics = "Regenerative Medicine, Social Graph Visualization, Covid-19, Stem Cells, Capitalism"  # TODO: replace with actual DB query
        response = self.send_single_prompt([test_topics, summarize_topics_prompt])
        topics = []
        edges = []  # TODO: populate edges
        try:
            json_array = json.loads(response.text)
            for d in json_array:
                topic = Topic(d)
                topics.append(topic)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        return topics
