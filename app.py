from flask import Flask, render_template, jsonify, make_response, request
from backend.memgraph.database.memgraph import Memgraph
from backend.memgraph import db_operations

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    db = Memgraph()
    db_operations.clear(db)
    db_operations.populate_database(db, "backend/resources/dev_data.txt")
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    paper_id = request.form['paper_id']
    # Now you can process the user input as needed
    # For example, you can print it or perform some operations
    print('Paper ID Input:', paper_id)
    return paper_id

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