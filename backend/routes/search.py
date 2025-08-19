from flask import Blueprint, request, jsonify
from models.translation import translate_to_english, translate_from_english
from sentence_transformers import SentenceTransformer, util
import json
import os
import torch
from flask_cors import CORS

search_bp = Blueprint("search", __name__)

# Enable CORS for this blueprint
CORS(search_bp, origins=["http://localhost:5173"], methods=["GET", "POST", "OPTIONS"])

# Load herbs DB
HERBS_DB_PATH = os.path.join(os.path.dirname(__file__), "../../database/data.json")
with open(HERBS_DB_PATH, "r", encoding="utf-8") as f:
    herbs_data = json.load(f)

# Load multilingual sentence transformer
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", device=device)

# Precompute herb embeddings with emphasis on names
herb_sentences = []
for h in herbs_data:
    # Create multiple variations for better matching
    name_variants = [h['name']]
    name_variants.extend(h.get('common_names', []))
    if 'languages' in h:
        name_variants.extend(h['languages'].values())
    
    # Create embedding text with repeated names for better name matching
    herb_text = f"{h['name']} {h['name']} {' '.join(name_variants)} {h.get('scientific_name', '')} {h.get('uses', '')}"
    herb_sentences.append(herb_text)

print(f"Herb embeddings created for {len(herb_sentences)} herbs")
for i, sentence in enumerate(herb_sentences):
    print(f"Herb {i}: {sentence[:100]}...")

herb_embeddings = model.encode(herb_sentences, convert_to_tensor=True)

def search_herbs(query: str):
    query_lower = query.strip().lower()

    # Stage 1: Direct / fuzzy match by name or aliases
    direct_matches = []
    for idx, h in enumerate(herbs_data):
        all_names = [h['name'].lower()]
        all_names.extend([n.lower() for n in h.get('common_names', [])])
        if 'languages' in h:
            all_names.extend([n.lower() for n in h['languages'].values()])

        if any(query_lower == n or query_lower in n for n in all_names):
            direct_matches.append((1.0, idx))  # perfect score

    if direct_matches:
        # Return only direct matches
        return [herbs_data[idx] for _, idx in direct_matches]

    # Stage 2: Semantic similarity fallback
    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, herb_embeddings)[0]
    similarity_scores = [(float(score), idx) for idx, score in enumerate(scores)]

    similarity_threshold = 0.5
    filtered_results = [
        (score, idx) for score, idx in similarity_scores if score >= similarity_threshold
    ]
    filtered_results.sort(reverse=True)

    # Return top matches
    return [herbs_data[idx] for _, idx in filtered_results[:5]]


@search_bp.route("/search", methods=["GET", "POST", "OPTIONS"])
def search():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response
    
    try:
        print("Received search request")        
        print("Received data:")
        print(request.headers)
        print("Received data1:")
        print(request.data)
        
        # Handle both GET and POST requests
        if request.method == "GET":
            query = request.args.get('q', '').strip()
        else:
            if not request.is_json:
                return jsonify({"status": "error", "message": "Invalid JSON format"}), 400
            # Fix: Check for both possible keys
            query = request.json.get('query', '') or request.json.get('inputMessage', '')
            query = query.strip()
        
        print("Received search request", query)

        if not query:
            return jsonify({"status": "error", "message": "Query is required"}), 400

        # Translate query to English
        english_query = translate_to_english(query)

        results = search_herbs(english_query)  # Call the search function to ensure it runs

        # # Compute similarity
        # query_embedding = model.encode(english_query, convert_to_tensor=True)
        # similarities = util.pytorch_cos_sim(query_embedding, herb_embeddings)[0]

        # # Get top matches (limit to available data) with similarity threshold
        # num_herbs = len(herbs_data)
        # k = min(5, num_herbs)  # Don't request more than available
        
        # if k == 0:
        #     return jsonify({"status": "error", "message": "No herbs data available"}), 404
        
        # # Get all similarities with their indices
        # similarity_scores = [(float(similarities[i]), i) for i in range(len(similarities))]
        
        # # Sort by similarity score (descending) and filter by threshold
        # similarity_threshold = 0.2  # Only return results with similarity > 0.3
        # filtered_results = [
        #     (score, idx) for score, idx in similarity_scores 
        #     if score > similarity_threshold
        # ]
        # filtered_results.sort(reverse=True)
        
        # # Take top k results
        # top_results = filtered_results[:k]
        # print(f"Top {k} results: {top_results}")
        # if not top_results:
        #     return jsonify([])  # Return empty array if no good matches

        # # Prepare response
        # original_lang = "en" if english_query == query else "hi"
        # results = []
        
        # for score, idx in top_results:
        #     herb = herbs_data[int(idx)].copy()  # Create a copy to avoid modifying original
            
        #     # Add similarity score for debugging (optional)
        #     herb["similarity_score"] = round(score, 3)
            
        #     # Translate if needed
        #     if original_lang != "en":
        #         herb["name"] = translate_from_english(herb["name"], original_lang)
        #         herb["uses"] = translate_from_english(herb["uses"], original_lang)
            
        #     results.append(herb)

        response = jsonify(results)
        print("Search results:")
        print(results)
        # Add CORS headers to the response
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        return response
        
    except Exception as e:
        print(f"Error in search: {e}")
        error_response = jsonify({"error": str(e)})
        error_response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        return error_response, 500