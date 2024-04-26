# Gemini client that connects to Google Gemini

import google.generativeai as genai
import json

from backend.global_methods import load_yaml_config, read_txt
from backend.topic import Topic
from backend.edge import Edge


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
    
    # Generates the L2 topics from paper abstract, and edges between the topics
    def generate_l2_topic_graph(self):
        prompt = read_txt(f"{self.prompts_path}/generate_l2_topic_graph.txt")
        test_abstracts = read_txt(f"{self.prompts_path}/sample_abstracts.txt")  # TODO: replace with actual DB query
        full_prompt = prompt + test_abstracts

        response = self.send_single_prompt(full_prompt)
        topics = []
        edges = []
        try:
            json_result = json.loads(response.text)
            for d in json_result["topics"]:
                topic = Topic(d)
                topics.append(topic)
            for d in json_result["edges"]:
                edge = Edge(d)
                edges.append(edge)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        return (topics, edges)

    # Summarise L2 topics into L1 topics
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

    # === testing ===
    # For testing L2 topics generation 
    def test_generate_topics_from_abstracts(self):
        generate_topics_prompt = read_txt(f"{self.prompts_path}/generate_topics.txt")
        test_abstracts = read_txt(f"{self.prompts_path}/sample_abstracts.txt")  # TODO: replace with actual DB query
        response = self.send_single_prompt([test_abstracts, generate_topics_prompt])
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

    # For testing edge generation
    # actual edge generation is combined into generate_l2_topic_graph
    def test_generate_edges(self):
        prompt = read_txt(f"{self.prompts_path}/generate_topic_edges.txt")
        test_topics = read_txt(f"{self.prompts_path}/sample_topics.txt")
        # full_prompt = generate_edges_prompt.format(input=test_topics)
        # full_prompt = generate_edges_prompt
        full_prompt = prompt + test_topics
        print(full_prompt)
        response = self.send_single_prompt(full_prompt)
        edges = []
        try:
            json_array = json.loads(response.text)
            for d in json_array:
                edge = Edge(d)
                edges.append(edge)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        return edges
