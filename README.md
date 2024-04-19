# pipripv2_mvp

## Arxiv API
- API downloading, iterate recursively (configurable depth) through the references
- Seed is paper from user input 
- References hopefully we download from the API
- https://info.arxiv.org/help/api/basics.html


## Setup
To setup local environment:
- create a folder called "papers_cache"
- python -m venv env (if it does not run, open powershell as admin and do it in the project's root folder)
- .\env\Scripts\activate
- pip install -r requirements.txt
- pip install -q -U google-generativeai
- deactivate << to exit and enter another environment (e.g., if I have multiple python projects)

## Potential libraries to use
- https://github.com/kandiraju/arxiv_data_extraction
- https://github.com/lukasschwab/arxiv.py
- https://github.com/memgraph/sng-demo (Social Network Graph)
----

## Run UI
```
docker-compose build
docker-compose up
```
Open an incognito window and go to localhost:5000.

To close container, type: (Stops all running containers at once)
```
docker stop $(docker ps -aq)
```

## Gemini Client
- Set up file called <api_key.yaml> in 'gemini/config/'
- Add in "GEMINI_API_KEY: <your api key>"
- python -m venv env (if it does not run, open powershell as admin and do it in the project's root folder)
- .\env\Scripts\activate
- pip install -q -U google-generativeai