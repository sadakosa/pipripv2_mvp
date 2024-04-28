from flask import Flask, render_template, jsonify, make_response, request

from backend.graph_manager import build_graph_from_paper_ids
from backend.memgraph.database.memgraph import Memgraph
from backend.memgraph import db_operations
from backend.memgraph.query_generator import generate_queries_for_graph
import re

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    # db = Memgraph()
    # db_operations.clear(db)
    # db_operations.populate_database(db, "backend/resources/dev_data.txt")
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    paper_id = request.form['paper_id']

    # Input validation
    arxiv_id_pattern = r'\d+\.\d+'
    arxiv_ids = []
    ss_ids = []
    if bool(re.match(arxiv_id_pattern, paper_id)):
        arxiv_ids.append(paper_id)
    elif len(paper_id) == 40 and paper_id.islower() and paper_id.isalnum():
        ss_ids.append(paper_id)

    # Build graph, add nodes and edges to DB
    db = Memgraph()
    db_operations.clear(db)
    print('Paper ID Input:', paper_id)
    graph = build_graph_from_paper_ids(arxiv_ids, ss_ids)
    queries = generate_queries_for_graph(graph)
    for q in queries:
        db.execute_query(q)

    return render_template('index.html')

@app.route('/query')
def query():
    return render_template('query.html')

@app.route("/get-graph", methods=["POST"])
def get_graph():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_graph(db)), 200)
    return response

@app.route('/get-nodes', methods=["POST"])
def get_nodes():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_nodes(db)), 200)
    return response

@app.route('/get-relationships', methods=["POST"])
def get_relationships():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_relationships(db)), 200)
    return response