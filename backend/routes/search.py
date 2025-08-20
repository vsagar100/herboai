import json
import os
import sys
from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer, util
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#import database.db
from database.db import HerbalDataFetcher

# Main API Blueprint - Single entry point for frontend
search_bp = Blueprint("api", __name__)

# Load model and data
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

#DATA_FILE = os.path.join(os.path.dirname(__file__), "../../database/data.json")
# with open(DATA_FILE, "r", encoding="utf-8") as f:
#     HERB_DATA = json.load(f)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database\\herboai.db')
print(f"Using database at: {DB_PATH}")
fetcher = HerbalDataFetcher(DB_PATH)
HERB_DATA = fetcher.fetch_all_herbs()

class RequestAnalyzer:
    """Analyzes incoming requests to determine the best response strategy"""

    @staticmethod
    def analyze_query(query, request_context=None):
        if not query or not query.strip():
            return {"action": "error", "confidence": 1.0, "metadata": {"error": "Empty query"}}

        query = query.strip()
        word_count = len(query.split())
        char_count = len(query)

        if RequestAnalyzer._is_suggestion_request(query, request_context):
            return {
                "action": "suggest",
                "confidence": 0.9,
                "metadata": {"query_type": "partial", "word_count": word_count},
            }

        if RequestAnalyzer._is_search_request(query):
            search_strategy = RequestAnalyzer._determine_search_strategy(query)
            return {
                "action": "search",
                "confidence": 0.95,
                "metadata": {
                    "query_type": "complete",
                    "strategy": search_strategy,
                    "word_count": word_count,
                    "char_count": char_count,
                },
            }

        return {"action": "search", "confidence": 0.7, "metadata": {"query_type": "ambiguous", "word_count": word_count}}

    @staticmethod
    def _is_suggestion_request(query, context):
        if len(query) <= 2:
            return True
        if context and context.get("typing", False):
            return True
        if len(query) <= 4 and len(query.split()) == 1:
            return True
        return False

    @staticmethod
    def _is_search_request(query):
        herb_names = [herb.get("name", "").lower() for herb in HERB_DATA]
        alt_names = []
        for herb in HERB_DATA:
            alt_names.extend(herb.get("common_names", []))
            if "languages" in herb:
                alt_names.extend(list(herb["languages"].values()))

        if query.lower() in herb_names or query.lower() in [n.lower() for n in alt_names]:
            return True
        if len(query) >= 3:
            return True
        return False

    @staticmethod
    def _determine_search_strategy(query):
        query_lower = query.lower()
        word_count = len(query.split())

        herb_names = [herb.get("name", "").lower() for herb in HERB_DATA]
        if query_lower in herb_names:
            return "exact_match"

        health_keywords = [
            "pain",
            "stress",
            "immunity",
            "digestion",
            "sleep",
            "skin",
            "hair",
            "cold",
            "fever",
            "headache",
            "joint",
            "memory",
            "energy",
            "detox",
        ]
        if any(keyword in query_lower for keyword in health_keywords):
            return "symptom_based"

        if word_count == 1:
            return "single_term"
        if word_count > 3:
            return "semantic"

        return "hybrid"


class IntelligentHerbalSearch:
    def __init__(self, HERB_DATA, model):
        self.HERB_DATA = HERB_DATA
        self.model = model
        self.prepare_search_data()

    def prepare_search_data(self):
        self.name_index = {}
        self.alt_name_index = {}
        self.semantic_texts = []
        self.keyword_texts = []

        for i, herb in enumerate(self.HERB_DATA):
            herb_name = herb.get("name", "").lower().strip()
            self.name_index[herb_name] = i

            # Collect alt names (common_names + languages.*)
            alt_names = []
            alt_names.extend(herb.get("common_names", []))
            if "languages" in herb:
                alt_names.extend(list(herb["languages"].values()))

            for alt in alt_names:
                self.alt_name_index[alt.lower().strip()] = i

            # Semantic parts
            semantic_parts = [
                herb.get("name", ""),
                herb.get("scientific_name", ""),
                " ".join(alt_names),
                herb.get("uses", ""),
                herb.get("ayush_system", ""),
            ]
            for rem in herb.get("remedies", []):
                semantic_parts.append(rem.get("condition", ""))
                semantic_parts.append(rem.get("preparation", ""))

            self.semantic_texts.append(" ".join(filter(None, semantic_parts)))

            # Keyword parts
            keyword_parts = [herb.get("name", ""), " ".join(alt_names), herb.get("uses", "")]
            self.keyword_texts.append(" ".join(filter(None, keyword_parts)).lower())

        print("Creating semantic embeddings...")
        self.semantic_embeddings = self.model.encode(
            self.semantic_texts, convert_to_tensor=True, normalize_embeddings=True, show_progress_bar=True
        )

        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 3), lowercase=True, max_features=5000)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.keyword_texts)

    def search(self, query, strategy="hybrid"):
        if not query or not query.strip():
            return []
        query = query.strip()

        if strategy == "exact_match":
            return self._exact_match_search(query)
        elif strategy == "single_term":
            return self._single_term_search(query)
        elif strategy == "symptom_based":
            return self._symptom_based_search(query)
        elif strategy == "semantic":
            return self._symptom_based_search(query)
        else:
            return self._hybrid_search(query)

    def _exact_match_search(self, query):
        q = query.lower().strip()
        results = []
        if q in self.name_index:
            results.append({"herb": self.HERB_DATA[self.name_index[q]], "score": 1.0, "match_type": "exact_name"})
        if q in self.alt_name_index:
            idx = self.alt_name_index[q]
            if not any(r["herb"]["name"] == self.HERB_DATA[idx]["name"] for r in results):
                results.append({"herb": self.HERB_DATA[idx], "score": 0.95, "match_type": "alt_name"})
        return results

    def _single_term_search(self, query):
        results = []
        seen = set()

        exact_results = self._exact_match_search(query)
        for r in exact_results:
            results.append(r)
            seen.add(r["herb"]["name"])

        if not exact_results:
            q = query.lower()
            for herb in self.HERB_DATA:
                if herb["name"] in seen:
                    continue
                if q in herb.get("name", "").lower():
                    results.append({"herb": herb, "score": 0.8, "match_type": "partial_name"})
                    seen.add(herb["name"])
                    continue
                alt_names = herb.get("common_names", [])
                if "languages" in herb:
                    alt_names.extend(list(herb["languages"].values()))
                for alt in alt_names:
                    if q in alt.lower():
                        results.append({"herb": herb, "score": 0.75, "match_type": "partial_alt_name"})
                        seen.add(herb["name"])
                        break
        return sorted(results, key=lambda x: x["score"], reverse=True)[:5]

    def _symptom_based_search(self, query):
        q_emb = self.model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
        scores = util.cos_sim(q_emb, self.semantic_embeddings)[0]

        results = []
        for i, score in enumerate(scores):
            if float(score) >= 0.25:
                results.append({"herb": self.HERB_DATA[i], "score": float(score), "match_type": "semantic"})
        return sorted(results, key=lambda x: x["score"], reverse=True)[:5]

    def _hybrid_search(self, query):
        results = []
        seen = set()
        exact = self._exact_match_search(query)
        for r in exact:
            if r["herb"]["name"] not in seen:
                results.append(r)
                seen.add(r["herb"]["name"])
        if len(results) < 3:
            semantic = self._symptom_based_search(query)
            for r in semantic:
                if r["herb"]["name"] not in seen and len(results) < 5:
                    results.append(r)
                    seen.add(r["herb"]["name"])
        return sorted(results, key=lambda x: x["score"], reverse=True)[:5]

    def get_suggestions(self, partial_query):
        if len(partial_query) < 2:
            return []
        q = partial_query.lower()
        suggestions = []
        for herb in self.HERB_DATA:
            if q in herb.get("name", "").lower():
                suggestions.append({"text": herb["name"], "type": "herb_name"})
            alt_names = herb.get("common_names", [])
            if "languages" in herb:
                alt_names.extend(list(herb["languages"].values()))
            for alt in alt_names:
                if q in alt.lower():
                    suggestions.append({"text": alt, "type": "alt_name", "herb": herb["name"]})
            if q in herb.get("uses", "").lower():
                suggestions.append({"text": f"{herb['uses']} ({herb['name']})", "type": "use_case", "herb": herb["name"]})
        seen = set()
        unique = []
        for s in suggestions:
            if s["text"] not in seen:
                unique.append(s)
                seen.add(s["text"])
        return unique[:8]


print("Initializing AYUSH Herbal Search System...")
search_system = IntelligentHerbalSearch(HERB_DATA, model)
print("Search system ready!")


@search_bp.route("/query", methods=["POST"])
def handle_query():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        context = data.get("context", {})
        if not query:
            return jsonify({"success": False, "error": "Query required"}), 400

        analysis = RequestAnalyzer.analyze_query(query, context)
        if analysis["action"] == "error":
            return jsonify({"success": False, "error": analysis["metadata"]["error"]}), 400
        elif analysis["action"] == "suggest":
            suggestions = search_system.get_suggestions(query)
            return jsonify({"success": True, "action": "suggest", "query": query, "suggestions": suggestions})
        elif analysis["action"] == "search":
            strategy = analysis["metadata"].get("strategy", "hybrid")
            results = search_system.search(query, strategy)
            return jsonify({"success": True, "action": "search", "query": query, "results": results})
        else:
            return jsonify({"success": False, "error": "Unknown action"}), 400
    except Exception as e:
        print(f"API Error: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@search_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "model": "paraphrase-multilingual-mpnet-base-v2", "total_herbs": len(HERB_DATA)})


@search_bp.route("/search", methods=["POST"])
def direct_search():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        strategy = data.get("strategy", "hybrid")
        results = search_system.search(query, strategy)
        return jsonify({"query": query, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@search_bp.route("/suggest", methods=["POST"])
def direct_suggest():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        suggestions = search_system.get_suggestions(query)
        return jsonify({"query": query, "suggestions": suggestions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
