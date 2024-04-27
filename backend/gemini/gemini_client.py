# Gemini client that connects to Google Gemini

import google.generativeai as genai
import json

from backend.global_methods import load_yaml_config, read_txt
from backend.paper import Paper
from backend.topic import Topic
from backend.edge import Edge

# Constants
NUM_RETRIES = 5

class GeminiClient:
    def __init__(self):
        # load the prompts
        self.prompts_path = 'backend/gemini/prompts'
        # self.starter_sys_prompt = read_txt(f"{self.prompts_path}/starter.txt")

        # load the api key
        config = load_yaml_config('backend/gemini/config/api_key.yaml')
        api_key = config['GEMINI_API_KEY']
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel('gemini-pro')

    # to deal with the fact that there is no system prompt in the gemini api, we will just use the starting user prompt as the system prompt
    # link: https://www.reddit.com/r/Bard/comments/1b90i8o/does_gemini_have_a_system_prompt_option_while/
    # link: https://www.googlecloudcommunity.com/gc/AI-ML/Gemini-Pro-Context-Option/m-p/684704/highlight/true#M4159
    # def send_starter_system_prompt(self):
    #     response = self.client.generate_content(self.starter_sys_prompt)
    #     print(response.text)
    #     return response

    def send_single_prompt(self, prompt):
        response = self.client.generate_content(prompt)
        # print(response.text)
        return response

    # Convert paper to a json string for input to Gemini
    def convert_papers_to_json_string(self, papers: list[Paper]):
        paper_json_strings = []
        for paper in papers:
            input_dict = {
                "id": paper.paper_id,
                "title": paper.title,
                "abstract": paper.abstract
            }
            paper_json_strings.append(json.dumps(input_dict))
        return ",\n".join(paper_json_strings)

    # Generates the L2 topics from paper title and abstract, and edges between the topics
    def generate_l2_topics_and_edges(self, papers: list[Paper]):
        prompt = read_txt(f"{self.prompts_path}/generate_l2_topic_graph.txt")
        papers_json_string = self.convert_papers_to_json_string(papers)

        topics = []
        edges = []
        success = False
        # Retry for NUM_RETRIES times, because sometimes the output may not be correct JSON or empty
        for i in range(NUM_RETRIES):
            if success:
                break
            # Send request to gemini
            print("Generating L2 topics and edges...")
            response = self.send_single_prompt([papers_json_string, prompt])
            try:
                json_result = json.loads(response.text)
                for d in json_result["topics"]:
                    if not d.get("paper_ids"):  # skip topics with no linked papers
                        continue
                    topic = Topic(d)
                    topics.append(topic)
                    # paper-topic edges
                    for paper_id in d.get("paper_ids"):
                        edge = Edge({
                            "source_type": "Paper",
                            "target_type": "Topic",
                            "source": paper_id,
                            "target": topic.id,
                            "label": "relates_to"
                        })
                        edges.append(edge)
                for d in json_result["edges"]:
                    d['label'] = d.get('label').replace(" ", "_")
                    edge = Edge(d)
                    edge.source_type = "Topic"
                    edge.target_type = "Topic"
                    edges.append(edge)

                success = True
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                continue
            
        return topics, edges

    # Summarise L2 topics into L1 topics, and generate edges between the topics
    def generate_l1_topics_and_edges(self, l2_topics: list[Topic]):
        prompt = read_txt(f"{self.prompts_path}/generate_l1_topic_graph.txt")
        topic_ids = [t.id for t in l2_topics]

        topics = []
        edges = []
        success = False
        # Retry for NUM_RETRIES times, because sometimes the output may not be correct JSON or empty
        for i in range(NUM_RETRIES):
            if success:
                break
            # Send request to gemini
            print("Generating L1 topics and edges...")
            response = self.send_single_prompt([', '.join(topic_ids), prompt])
            try:
                json_result = json.loads(response.text)
                for d in json_result["topics"]:
                    if not d.get("topic_ids"):  # skip topics with no linked topics
                        continue
                    topic = Topic(d)
                    topics.append(topic)
                    for topic_id in d.get("topic_ids"):
                        edge = Edge({
                            "source_type": "Topic",
                            "target_type": "Topic",
                            "source": topic_id,
                            "target": topic.id,
                            "label": "is_subset_of"
                        })
                        edges.append(edge)
                for d in json_result["edges"]:
                    d['label'] = d.get('label').replace(" ", "_")
                    edge = Edge(d)
                    edge.source_type = "Topic"
                    edge.target_type = "Topic"
                    edges.append(edge)

                success = True
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                continue

        return topics, edges

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

    # For testing edge generation
    # actual edge generation is combined into generate_l2_topic_graph & generate_l1_topic_graph
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
