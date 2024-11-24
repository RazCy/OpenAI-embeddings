import json
from search_in_pinecone import search_in_pinecone
from flask import Flask, request, jsonify,render_template


app = Flask(__name__)

# Load embeddings
#embeddings = load_embeddings(embeddings_file)

@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/search", methods=["POST"])
def search():
    #query = request.json.get("query")
    print(request.form)
    query =  request.form['query']
    print(query)
    if not query:
        return jsonify({"error": "Query not provided"}), 400

    result = search_in_pinecone(query)
    print(result["matches"][0]["metadata"])
    return jsonify(result["matches"][0]["metadata"])
    #return json.dumps(result["matches"][0]["metadata"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
