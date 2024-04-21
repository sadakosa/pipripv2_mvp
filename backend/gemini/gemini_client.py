# gemini client that connects to gemini

#create access to the Google Gemini AI
import google.generativeai as genai

from backend.global_methods import load_yaml_config, read_txt

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
        generate_topics_prompt = read_txt(f"{self.prompts_path}/generate_topics.txt")
        test_abstracts = read_txt(f"{self.prompts_path}/sample_abstracts.txt")
        response = self.send_single_prompt([test_abstracts, generate_topics_prompt])
        return response

    def summarize_topics(self):
        summarize_topics_prompt = read_txt(f"{self.prompts_path}/summarize_topics.txt")
        test_topics = "Regenerative Medicine, Social Graph Visualization, Covid-19, Stem Cells, Capitalism"
        response = self.send_single_prompt([test_topics, summarize_topics_prompt])
        return response
