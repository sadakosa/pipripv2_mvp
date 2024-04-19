import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

def initialise_model():
    vertexai.init(project="banded-nimbus-420222", location="asia-southeast1") #initialise Vertex AI with project name and location
    gemini_model = GenerativeModel(model_name="gemini-1.5-pro-preview-0409") #latest model of Gemini AI
    return gemini_model

def start_chat(model):
    chat = model.start_chat()
    chat.send_message(open("backend/gemini_instructions.txt").read()) #first send the instructions upon starting chat
    return chat

def get_chat_response(chat, prompt):
    response = chat.send_message(prompt)
    return response

