import json
import os
from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer, util
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime, timedelta
import uuid
import hashlib
import threading
from collections import defaultdict

# Local utils
from database.db_utils import fetch_all_herbs
from utils.translator import translate_text

import unicodedata

# Main API Blueprint
search_bp = Blueprint("api", __name__)

# Devanagari helpers
_MARATHI_ONLY = set("ळऱवञझ")
_HINDI_ONLY = set("ड़ढ़ऩऱफ़ज़क़ख़ग़य़")

def _normalize(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    return s.strip().lower()

def _is_devanagari(text: str) -> bool:
    return any('\u0900' <= ch <= '\u097F' for ch in text)

def _guess_hi_or_mr(text: str) -> str:
    """Better heuristic for Hindi vs Marathi detection."""
    t = set(text)
    if t & _MARATHI_ONLY:
        return "mr"
    if t & _HINDI_ONLY:
        return "hi"
    
    # Additional heuristics based on common words
    marathi_words = ['तुळस', 'आळू', 'काळा', 'पिळू']
    hindi_words = ['तुलसी', 'आलू', 'काला', 'पीला']
    
    for word in marathi_words:
        if word in text:
            return "mr"
    for word in hindi_words:
        if word in text:
            return "hi"
    
    return "hi"  # Default to Hindi for generic Devanagari

def _collect_variants(herb: dict) -> set:
    """Collect all name variants with better handling."""
    v = set()
    
    # Main name
    name = herb.get("name", "")
    if name:
        v.add(_normalize(name))
    
    # Scientific name
    sci_name = herb.get("scientific_name", "")
    if sci_name:
        v.add(_normalize(sci_name))
    
    # Alt names
    alt_names = herb.get("alt_names", []) or []
    if isinstance(alt_names, list):
        for alt in alt_names:
            if alt:
                v.add(_normalize(alt))
    elif isinstance(alt_names, str):
        v.add(_normalize(alt_names))
    
    # Common names
    common_names = herb.get("common_names", []) or []
    if isinstance(common_names, list):
        for cn in common_names:
            if cn:
                v.add(_normalize(cn))
    
    # Languages dict: {'hi': 'तुलसी', 'mr': 'तुळस', 'en': 'Holy Basil'}
    languages = herb.get("languages", {})
    if isinstance(languages, dict):
        for lang_code, text in languages.items():
            if text and isinstance(text, str):
                v.add(_normalize(text))
    
    # Translations list: [{'language_code':'hi','text':'तुलसी'}, ...]
    translations = herb.get("translations", [])
    if isinstance(translations, list):
        for trans in translations:
            if isinstance(trans, dict):
                text = trans.get("text", "")
                if text:
                    v.add(_normalize(text))
    
    # Remove empty strings
    return {variant for variant in v if variant and len(variant.strip()) > 0}

# Enhanced language detection
def detect_lang(query: str) -> str:    
    """Detect language with better accuracy."""
    query = query.strip()
    
    if _is_devanagari(query):
        return _guess_hi_or_mr(query)
    
    # Check for other Indic scripts
    if any('\u0980' <= ch <= '\u09FF' for ch in query):
        return "bn"  # Bengali
    if any('\u0A80' <= ch <= '\u0AFF' for ch in query):
        return "gu"  # Gujarati
    
    return "en"

# Backend-only Session Management
class BackendSessionManager:
    def __init__(self):
        self.sessions = {}  # user_id -> session_data
        self.session_lock = threading.RLock()
        self.cleanup_interval = 3600  # 1 hour
        self.max_session_age = 86400  # 24 hours
        self.last_cleanup = datetime.now()
    
    def _generate_user_id(self, request_info):
        """Generate consistent user ID from request info."""
        # Use IP + User-Agent hash as user identifier
        ip = request_info.get('remote_addr', 'unknown')
        user_agent = request_info.get('user_agent', 'unknown')
        
        # Create hash for privacy
        user_string = f"{ip}:{user_agent}"
        return hashlib.md5(user_string.encode()).hexdigest()[:16]
    
    def _cleanup_old_sessions(self):
        """Remove old sessions to prevent memory leak."""
        now = datetime.now()
        if (now - self.last_cleanup).seconds < self.cleanup_interval:
            return
        
        with self.session_lock:
            expired_sessions = []
            for user_id, session in self.sessions.items():
                if (now - session['last_activity']).seconds > self.max_session_age:
                    expired_sessions.append(user_id)
            
            for user_id in expired_sessions:
                del self.sessions[user_id]
            
            self.last_cleanup = now
            print(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def get_session(self, request_info):
        """Get or create session for user."""
        user_id = self._generate_user_id(request_info)
        
        with self.session_lock:
            self._cleanup_old_sessions()
            
            if user_id not in self.sessions:
                self.sessions[user_id] = {
                    'user_id': user_id,
                    'created_at': datetime.now(),
                    'last_activity': datetime.now(),
                    'query_history': [],
                    'language_preference': 'en',
                    'search_context': {},
                    'total_queries': 0
                }
            
            # Update last activity
            self.sessions[user_id]['last_activity'] = datetime.now()
            return self.sessions[user_id]
    
    def add_query(self, request_info, query, results, language):
        """Add query to user's history."""
        session = self.get_session(request_info)
        
        with self.session_lock:
            session['query_history'].append({
                'query': query,
                'language': language,
                'timestamp': datetime.now(),
                'results_count': len(results),
                'top_result': results[0]['herb'].get('name', '') if results else None
            })
            
            # Keep only last 20 queries
            if len(session['query_history']) > 20:
                session['query_history'] = session['query_history'][-20:]
            
            session['language_preference'] = language
            session['total_queries'] += 1
    
    def get_context(self, request_info):
        """Get user context for personalized responses."""
        session = self.get_session(request_info)
        
        recent_queries = session['query_history'][-5:] if session['query_history'] else []
        
        return {
            'recent_queries': [q['query'] for q in recent_queries],
            'language_preference': session['language_preference'],
            'total_queries': session['total_queries'],
            'session_age': (datetime.now() - session['created_at']).seconds
        }
    
    def get_stats(self):
        """Get session statistics."""
        with self.session_lock:
            return {
                'active_sessions': len(self.sessions),
                'total_queries': sum(s['total_queries'] for s in self.sessions.values()),
                'languages_used': list(set(s['language_preference'] for s in self.sessions.values()))
            }

# Query Analyzer with simplified logic
class RequestAnalyzer:
    @staticmethod
    def analyze_query(query, context=None):
        if not query or not query.strip():
            return {"action": "error", "confidence": 1.0,
                    "metadata": {"error": "Empty query"}}
        
        query = query.strip()
        word_count = len(query.split())
        
        # For very short queries, suggest
        if len(query) <= 2:
            return {"action": "suggest", "confidence": 0.7,
                    "metadata": {"query_type": "too_short"}}
        
        # Everything else is search
        strategy = RequestAnalyzer._determine_search_strategy(query, context)
        return {"action": "search", "confidence": 0.5,
                "metadata": {"query_type": "search", "strategy": strategy}}

    @staticmethod
    def _determine_search_strategy(query, context=None):
        query_lower = query.lower()
        word_count = len(query.split())
        
        # Single word gets single_term strategy
        if word_count == 1:
            return "single_term"
        
        # Health keywords get symptom search
        health_keywords = [
            "pain", "stress", "immunity", "digestion", "sleep", "skin", "hair", 
            "cold", "fever", "headache", "joint", "memory", "energy", "detox",
            "cough", "diabetes", "blood", "weight", "liver", "kidney"
        ]
        
        if any(keyword in query_lower for keyword in health_keywords):
            return "symptom_based"
        
        # Multi-word queries use hybrid
        return "hybrid"

# Load model and data
print("Loading model and data...")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
herbs_data = fetch_all_herbs()
session_manager = BackendSessionManager()

print(f"Loaded {len(herbs_data)} herbs")

class IntelligentHerbalSearch:
    def __init__(self, herbs_data, model):
        self.herbs_data = herbs_data
        self.model = model
        self.prepare_search_data()

    def prepare_search_data(self):
        """Prepare search indexes with debugging."""
        print("Preparing search indexes...")
        
        self.name_index = {}  # normalized_variant -> herb_index
        self.variant_map = {}  # herb_index -> set_of_variants
        self.semantic_texts = []
        self.keyword_texts = []
        
        variant_count = 0
        
        for i, herb in enumerate(self.herbs_data):
            # Collect variants for this herb
            variants = _collect_variants(herb)
            self.variant_map[i] = variants
            variant_count += len(variants)
            
            # Debug: Print variants for first few herbs
            if i < 3:
                print(f"Herb {i} ({herb.get('name', 'Unknown')}): {variants}")
            
            # Index each variant
            for variant in variants:
                if variant:  # Ensure not empty
                    self.name_index[variant] = i
            
            # Build semantic text
            semantic_parts = [
                herb.get("name", ""),
                herb.get("scientific_name", ""),
                " ".join(herb.get("alt_names", []) if isinstance(herb.get("alt_names"), list) else []),
                str(herb.get("uses", "")),
                " ".join(herb.get("therapies", []) if isinstance(herb.get("therapies"), list) else []),
            ]
            
            # Add multilingual names to semantic text
            if isinstance(herb.get("languages"), dict):
                semantic_parts.extend([v for v in herb["languages"].values() if v])
            
            self.semantic_texts.append(" ".join([p for p in semantic_parts if p]))
            
            # Build keyword text
            keyword_parts = [
                herb.get("name", ""),
                " ".join(herb.get("alt_names", []) if isinstance(herb.get("alt_names"), list) else [])
            ]
            
            if isinstance(herb.get("languages"), dict):
                keyword_parts.extend([v for v in herb["languages"].values() if v])
                
            self.keyword_texts.append(_normalize(" ".join([p for p in keyword_parts if p])))
        
        print(f"Created {len(self.name_index)} variant mappings from {variant_count} total variants")
        
        # Create embeddings
        print("Creating semantic embeddings...")
        self.semantic_embeddings = self.model.encode(
            self.semantic_texts,
            convert_to_tensor=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        
        # Create TF-IDF matrix
        print("Creating TF-IDF matrix...")
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words=None,
            lowercase=True,
            max_features=5000
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.keyword_texts)
        
        print("Search system ready!")

    def search(self, query, strategy="hybrid", context=None):
        """Main search function with debugging."""
        if not query.strip():
            return []
        
        query = query.strip()
        print(f"Searching: '{query}' with strategy: {strategy}")
        
        if strategy == "single_term":
            return self._single_term_search(query)
        elif strategy == "symptom_based":
            return self._semantic_search(query, threshold=0.15)
        elif strategy == "semantic":
            return self._semantic_search(query, threshold=0.25)
        else:  # hybrid
            return self._hybrid_search(query)

    def _single_term_search(self, query):
        """Fixed single term search with comprehensive debugging."""
        print(f"\n=== SINGLE TERM SEARCH DEBUG for '{query}' ===")
        
        normalized_query = _normalize(query)
        print(f"Normalized query: '{normalized_query}'")
        
        results = []
        
        # Step 1: Direct exact match
        print("Step 1: Checking direct exact match...")
        if normalized_query in self.name_index:
            herb_idx = self.name_index[normalized_query]
            herb = self.herbs_data[herb_idx]
            print(f"✓ Found exact match: {herb.get('name', 'Unknown')}")
            results.append({
                "herb": herb,
                "score": 1.0,
                "match_type": "exact_match"
            })
            return results
        else:
            print("✗ No exact match found")
        
        # Step 2: Partial matching
        print("Step 2: Checking partial matches...")
        partial_matches = []
        for variant, herb_idx in self.name_index.items():
            if normalized_query in variant:
                herb = self.herbs_data[herb_idx]
                score = len(normalized_query) / len(variant)  # Score based on coverage
                partial_matches.append({
                    "herb": herb,
                    "score": 0.7 + (score * 0.2),  # 0.7 to 0.9 range
                    "match_type": "partial_match",
                    "matched_variant": variant
                })
                print(f"✓ Partial match: '{variant}' -> {herb.get('name', 'Unknown')} (score: {score:.3f})")
        
        # Sort partial matches by score
        partial_matches.sort(key=lambda x: x["score"], reverse=True)
        results.extend(partial_matches[:5])
        
        # Step 3: Translation-based search for Devanagari
        if _is_devanagari(normalized_query):
            print("Step 3: Attempting translation-based search...")
            
            # Determine language and translate
            detected_lang = _guess_hi_or_mr(query)
            print(f"Detected Devanagari language: {detected_lang}")
            
            try:
                if detected_lang == "mr":
                    translated = translate_text(query, "mr", "en")
                else:
                    translated = translate_text(query, "hi", "en")
                
                print(f"Translated '{query}' -> '{translated}'")
                
                if translated and translated.lower() != query.lower():
                    normalized_translation = _normalize(translated)
                    
                    # Check exact match with translation
                    if normalized_translation in self.name_index:
                        herb_idx = self.name_index[normalized_translation]
                        herb = self.herbs_data[herb_idx]
                        print(f"✓ Translation exact match: {herb.get('name', 'Unknown')}")
                        results.append({
                            "herb": herb,
                            "score": 0.85,
                            "match_type": "translated_exact"
                        })
                    else:
                        # Check partial match with translation
                        for variant, herb_idx in self.name_index.items():
                            if normalized_translation in variant:
                                herb = self.herbs_data[herb_idx]
                                score = len(normalized_translation) / len(variant)
                                results.append({
                                    "herb": herb,
                                    "score": 0.6 + (score * 0.2),
                                    "match_type": "translated_partial",
                                    "matched_variant": variant
                                })
                                print(f"✓ Translation partial: '{variant}' -> {herb.get('name', 'Unknown')}")
                                break
                
            except Exception as e:
                print(f"Translation failed: {e}")
        
        # Step 4: Semantic search as fallback
        if not results:
            print("Step 4: Falling back to semantic search...")
            semantic_results = self._semantic_search(query, threshold=0.3)
            results.extend(semantic_results[:3])
            print(f"Added {len(semantic_results)} semantic results")
        
        # Remove duplicates and sort
        seen_herbs = set()
        unique_results = []
        for result in results:
            herb_name = result["herb"].get("name", "")
            if herb_name not in seen_herbs:
                unique_results.append(result)
                seen_herbs.add(herb_name)
        
        final_results = sorted(unique_results, key=lambda x: x["score"], reverse=True)[:5]
        print(f"=== FINAL RESULTS: {len(final_results)} herbs found ===\n")
        
        for i, result in enumerate(final_results):
            print(f"{i+1}. {result['herb'].get('name', 'Unknown')} (score: {result['score']:.3f}, type: {result['match_type']})")
        
        return final_results

    def _semantic_search(self, query, threshold=0.25):
        """Semantic search using embeddings."""
        try:
            query_embedding = self.model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
            scores = util.cos_sim(query_embedding, self.semantic_embeddings)[0]
            
            results = []
            for i, score in enumerate(scores):
                score_val = float(score)
                if score_val >= threshold:
                    results.append({
                        "herb": self.herbs_data[i],
                        "score": score_val,
                        "match_type": "semantic"
                    })
            
            return sorted(results, key=lambda x: x["score"], reverse=True)[:8]
        except Exception as e:
            print(f"Semantic search error: {e}")
            return []

    def _hybrid_search(self, query):
        """Hybrid search combining strategies."""
        results = []
        seen_herbs = set()
        
        # Try single term first if it's a single word
        if len(query.split()) == 1:
            single_results = self._single_term_search(query)
            for result in single_results:
                herb_name = result["herb"].get("name", "")
                if herb_name not in seen_herbs:
                    results.append(result)
                    seen_herbs.add(herb_name)
        
        # Add semantic results if needed
        if len(results) < 5:
            semantic_results = self._semantic_search(query, threshold=0.2)
            for result in semantic_results:
                herb_name = result["herb"].get("name", "")
                if herb_name not in seen_herbs:
                    results.append(result)
                    seen_herbs.add(herb_name)
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:8]

    def get_suggestions(self, partial_query):
        """Get suggestions for autocomplete."""
        if not partial_query or len(partial_query) < 1:
            return []
        
        normalized_partial = _normalize(partial_query)
        suggestions = []
        seen = set()
        
        for variant, herb_idx in self.name_index.items():
            if normalized_partial in variant and variant not in seen:
                herb = self.herbs_data[herb_idx]
                suggestions.append({
                    "text": variant,
                    "display_name": herb.get("name", ""),
                    "scientific_name": herb.get("scientific_name", "")
                })
                seen.add(variant)
                if len(suggestions) >= 8:
                    break
        
        return suggestions

# Initialize search system
print("Initializing search system...")
search_system = IntelligentHerbalSearch(herbs_data, model)

# API Routes
@search_bp.route("/query", methods=["POST"])
def handle_query():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()
        
        if not query:
            return jsonify({"success": False, "error": "Query required"}), 400

        # Get request info for session management
        request_info = {
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        }

        # Get user session and context
        context = session_manager.get_context(request_info)
        
        # Detect language
        detected_lang = detect_lang(query)
        print(f"\n[API] Query: '{query}' | Language: {detected_lang}")

        # Analyze query
        analysis = RequestAnalyzer.analyze_query(query, context)
        print(f"[API] Analysis: {analysis}")

        if analysis["action"] == "suggest":
            suggestions = search_system.get_suggestions(query)
            return jsonify({
                "success": True,
                "action": "suggest",
                "suggestions": suggestions,
                "query": query
            })

        # Perform search
        results = search_system.search(
            query, 
            analysis["metadata"].get("strategy", "hybrid"),
            context=context
        )

        # Add to user session
        session_manager.add_query(request_info, query, results, detected_lang)

        # Prepare response with translations if needed
        response_results = []
        for result in results:
            herb = result["herb"].copy()  # Don't modify original
            
            # Add display name in user's preferred language
            if detected_lang in ["hi", "mr"]:
                # Try to get native name
                if isinstance(herb.get("languages"), dict) and detected_lang in herb["languages"]:
                    herb["display_name"] = herb["languages"][detected_lang]
                else:
                    # Fallback to translation
                    try:
                        herb["display_name"] = translate_text(herb.get("name", ""), "en", detected_lang)
                    except:
                        herb["display_name"] = herb.get("name", "")
            else:
                herb["display_name"] = herb.get("name", "")
            
            # Add translated uses
            uses = herb.get("uses", "")
            if uses and detected_lang in ["hi", "mr"]:
                try:
                    if isinstance(uses, list):
                        uses_text = ". ".join(uses)
                    else:
                        uses_text = str(uses)
                    herb["uses_translated"] = translate_text(uses_text, "en", detected_lang)
                except:
                    herb["uses_translated"] = uses_text
            
            response_results.append({
                "herb": herb,
                "score": result["score"],
                "match_type": result["match_type"]
            })

        return jsonify({
            "success": True,
            "action": "search",
            "query": query,
            "results": response_results,
            "analysis": analysis,
            "language": detected_lang,
            "context": {
                "recent_queries": context.get("recent_queries", [])[-3:],
                "total_results": len(results),
                "session_queries": context.get("total_queries", 0)
            }
        })

    except Exception as e:
        print(f"Error in handle_query: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@search_bp.route("/suggestions", methods=["POST"])
def get_suggestions():
    try:
        data = request.get_json(force=True)
        partial_query = data.get("query", "").strip()
        
        suggestions = search_system.get_suggestions(partial_query)
        
        return jsonify({
            "success": True,
            "suggestions": suggestions,
            "query": partial_query
        })

    except Exception as e:
        print(f"Error in suggestions: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@search_bp.route("/health", methods=["GET"])
def health_check():
    stats = session_manager.get_stats()
    return jsonify({
        "status": "healthy",
        "total_herbs": len(herbs_data),
        "indexed_variants": len(search_system.name_index),
        "search_system": "ready",
        "session_stats": stats
    })

@search_bp.route("/debug/herb/<int:herb_id>", methods=["GET"])
def debug_herb(herb_id):
    """Debug endpoint to see herb variants."""
    if herb_id >= len(herbs_data):
        return jsonify({"error": "Herb not found"}), 404
    
    herb = herbs_data[herb_id]
    variants = _collect_variants(herb)
    
    return jsonify({
        "herb": herb,
        "variants": list(variants),
        "indexed_variants": {v: search_system.name_index.get(v, "NOT_FOUND") for v in variants}
    })

@search_bp.route("/debug/search/<query>", methods=["GET"])
def debug_search(query):
    """Debug endpoint to see search process."""
    normalized = _normalize(query)
    is_devanagari = _is_devanagari(query)
    detected_lang = detect_lang(query)
    
    # Check direct matches
    exact_match = normalized in search_system.name_index
    partial_matches = [v for v in search_system.name_index.keys() if normalized in v]
    
    return jsonify({
        "query": query,
        "normalized": normalized,
        "is_devanagari": is_devanagari,
        "detected_language": detected_lang,
        "exact_match": exact_match,
        "partial_matches": partial_matches[:10],
        "total_variants": len(search_system.name_index)
    })