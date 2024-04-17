# gemini client that connects to gemini

#create access to the Google Gemini AI
import google.generativeai as genai
import sys
from pathlib import Path

# Add the parent directory to sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Import module
from global_methods import read_txt, load_yaml_config
from logs.logger import Logger

# Remember to remove the parent directory from sys.path when done to avoid potential conflicts
sys.path.remove(str(parent_dir))

class GeminiClient:
    def __init__(self):
        # load the prompts
        starter_path = current_dir/ 'prompts/starter.txt'
        self.starter_sys_prompt = read_txt(starter_path)

        # load the api key
        config = load_yaml_config(current_dir/ 'config/api_key.yaml')
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