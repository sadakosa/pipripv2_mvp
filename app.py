from flask import Flask, render_template, jsonify, make_response, request

from backend.graph_manager import build_graph_from_paper_ids
from backend.memgraph.database.memgraph import Memgraph
from backend.memgraph import db_operations
from backend.memgraph.query_generator import generate_queries_for_graph
import re

app = Flask(__name__)
db = Memgraph()

@app.route('/')
@app.route('/index')
def index():
    # db = Memgraph()
    # db_operations.clear(db)
    # db_operations.populate_database(db, "backend/resources/dev_data.txt")
    return render_template('index.html')

@app.route('/clear_db', methods=['POST'])
def clear_db():
    db_operations.clear(db)
    # print(db_operations.get_topic_topic_edges(db), 1)
    # db_operations.delete_topic_topic_edges(db)
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    paper_id = request.form['paper_id']
    get_citations = request.form.get('citations_checkbox') == 'on'
    get_references = request.form.get('references_checkbox') == 'on'

    # Input validation
    arxiv_id_pattern = r'\d+\.\d+'
    arxiv_ids = []
    ss_ids = []
    if bool(re.match(arxiv_id_pattern, paper_id)):
        arxiv_ids.append(paper_id)
    elif len(paper_id) == 40 and paper_id.islower() and paper_id.isalnum():
        ss_ids.append(paper_id)

    # Retrieve existing topics to regenerate the topic-topic edges
    existing_topics = db_operations.get_topics(db)

    # Build graph, add nodes and edges to DB
    graph = build_graph_from_paper_ids(arxiv_ids, ss_ids, get_citations, get_references, existing_topics)
    queries = generate_queries_for_graph(graph)
    db_operations.delete_topic_topic_edges(db)
    for q in queries:
        db.execute_query(q)

    return render_template('index.html')

@app.route('/query')
def query():
    return render_template('query.html')

@app.route("/get-graph", methods=["POST"])
def get_graph():
    response = make_response(
        jsonify(db_operations.get_graph(db)), 200)
    return response

@app.route('/get-nodes', methods=["POST"])
def get_nodes():
    response = make_response(
        jsonify(db_operations.get_nodes(db)), 200)
    return response

@app.route('/get-relationships', methods=["POST"])
def get_relationships():
    response = make_response(
        jsonify(db_operations.get_relationships(db)), 200)
    return response