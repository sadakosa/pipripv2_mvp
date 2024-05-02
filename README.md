# PiP RIP 
### _Papers into Perspectives – Research Intelligence Processor_

### Introduction
Have you ever found yourself embarking on a research project, only to feel overwhelmed the moment you start exploring the topic? It's a common hurdle for researchers and students alike—entering a keyword and being inundated with hundreds of papers, each seemingly more complex than the last.

With so much data at our fingertips, how can we discern what's truly important and relevant, and quickly make sense of our research? Learning often happens when one begins making connections between concepts and topics. If only there was a way to obtain a bird eye's view of the available literature and visualize the connections between papers in an intuitive manner!

This is what we strive to accomplish in our hackathon project, titled **Papers into Perspectives – Research Intelligence Processor**. PiPRIP is a Gemini-powered knowledge graph generator that picks up key topics from the provided research papers and builds connections between those topics. By combining Gemini's LLM capabilities with the unique features of a graph data structure, our tool automates the process of knowledge visualization.

PiPRIP's generated knowledge graph enables users to:
- Identify relationships between papers at a glance
- Conveniently discover papers with overlapping topics
- Trace the citations/references lineage of papers, to understand how the research evolves over time

### Main features


### Tech overview
Semantic Scholar
ArXiv API
Google Gemini API
D3.js
Memgraph

---
### Setup and testing instructions
Gemini Client
- Set up file called <api_key.yaml> in 'gemini/config/'
- Add in "GEMINI_API_KEY: <your api key>"

You will require Docker desktop to build and run the Docker container.
```
docker-compose build
docker-compose up
```
Open an incognito browser window and browse the UI at localhost:5000.

---
PiPRIP is built by @chelchia, @g-lilian and @sadakosa.
Credit goes to https://github.com/memgraph/sng-demo for their demo of how to set up a social network graph visualization using D3 and Memgraph.
