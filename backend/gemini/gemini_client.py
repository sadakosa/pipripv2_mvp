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
        self.prompts_path = 'backend/gemini/prompts'

        config = load_yaml_config('backend/gemini/config/api_key.yaml')
        api_key = config['GEMINI_API_KEY']
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel('gemini-pro')

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

    # Generates the L2 topics, and topic-paper edges, from paper title and abstract
    def generate_l2_topics_and_edges(self, papers: list[Paper]):
        prompt = read_txt(f"{self.prompts_path}/generate_l2_topics_and_edges.txt")
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
                for d in json_result:
                    if not d.get("paper_ids"):  # skip topics with no linked papers
                        continue
                    topic = Topic({
                        "id": d.get("id"),
                        "description": d.get("description")
                    })
                    topics.append(topic)
                    # paper-topic edges
                    for paper_id in d.get("paper_ids"):
                        edge = Edge({
                            "source_type": "Paper",
                            "target_type": "TopicL2",
                            "source": paper_id,
                            "target": topic.id,
                            "label": "relates_to"
                        })
                        edges.append(edge)

                print(f"{len(topics)} topics and {len(edges)} edges generated.")
                success = True
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                continue
            
        return topics, edges

    def hydrate_l1_topic_descriptions(self, l1_topic_ids):
        prompt = read_txt(f"{self.prompts_path}/hydrate_topic_descriptions.txt")

        success = False
        hydrated_topics = []
        for i in range(NUM_RETRIES):
            if success:
                break
            # Send request to gemini
            print("Hydrating L1 topic descriptions...")
            response = self.send_single_prompt([', '.join(l1_topic_ids), prompt])
            try:
                json_result = json.loads(response.text)
                for d in json_result:
                    if d.get("id", "") in l1_topic_ids:
                        topic = Topic(d)
                        hydrated_topics.append(topic)
                success = True
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                continue

        return hydrated_topics

    # Summarise L2 topics into broader L1 topics, and generate edges between the topics
    def generate_l1_topics_and_edges(self, l2_topics: list[Topic]):
        prompt = read_txt(f"{self.prompts_path}/generate_l1_topics.txt")
        topic_ids = [t.id for t in l2_topics]

        edges = []
        success = False
        existing_topic_ids = set([t.id for t in l2_topics])
        new_topic_ids = set()
        # Retry for NUM_RETRIES times, because sometimes the output may not be correct JSON or empty
        for i in range(NUM_RETRIES):
            if success:
                break
            # Send request to gemini
            print("Generating L1 topics and edges...")
            response = self.send_single_prompt([', '.join(topic_ids), prompt])
            try:
                json_result = json.loads(response.text)
                for e in json_result:
                    source = e.get("source")
                    target = e.get("target")
                    source_type = "TopicL2" if source in existing_topic_ids else "TopicL1"
                    target_type = "TopicL2" if target in existing_topic_ids else "TopicL1"
                    edge = Edge({
                        "source_type": source_type,
                        "target_type": target_type,
                        "source": source,
                        "target": target,
                        "label": e.get("label").replace(" ", "_")
                    })
                    edges.append(edge)
                    if source not in existing_topic_ids:
                        new_topic_ids.add(source)
                    if target not in existing_topic_ids:
                        new_topic_ids.add(target)

                print(f"{len(new_topic_ids)} topics and {len(edges)} edges generated.")
                success = True
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                continue

        new_topics = self.hydrate_l1_topic_descriptions(new_topic_ids)

        return new_topics, edges

    # Generate new edges between topics. Currently only used for L1 topics.
    def generate_topic_topic_edges(self, topics):
        prompt = read_txt(f"{self.prompts_path}/generate_topic_edges.txt")
        topic_ids = [t.id for t in topics]

        edges = []
        success = False
        for i in range(NUM_RETRIES):
            if success:
                break
            # Send request to gemini
            print("Generating topic-topic edges...")
            response = self.send_single_prompt([', '.join(topic_ids), prompt])
            try:
                json_result = json.loads(response.text)
                for e in json_result:
                    edge = Edge({
                        "source_type": "TopicL1",
                        "target_type": "TopicL1",
                        "source": e.get("source"),
                        "target": e.get("target"),
                        "label": e.get("label").replace(" ", "_")
                    })
                    edges.append(edge)

                print(f"{len(edges)} L1 topic-topic edges generated.")
                success = True
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", e)
                continue

        return edges

    # === testing ===
    # For testing L2 topics generation 
    def test_generate_topics_from_abstracts(self):
        generate_topics_prompt = read_txt(f"{self.prompts_path}/generate_topics.txt")
        test_abstracts = read_txt(f"{self.prompts_path}/sample_abstracts.txt")
        response = self.send_single_prompt([test_abstracts, generate_topics_prompt])
        topics = []
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
        test_topics = "Regenerative Medicine, Social Graph Visualization, Covid-19, Stem Cells, Capitalism"
        response = self.send_single_prompt([test_topics, summarize_topics_prompt])
        topics = []
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
