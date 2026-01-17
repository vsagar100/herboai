#!/usr/bin/env python3
"""
Test Marathi query pipeline to identify translation issues.
"""
import sys
sys.path.insert(0, "/data/backend" if __import__("os").path.exists("/data/backend") else ".")

from flask import Flask
from run import create_app

# Create Flask context
app = create_app()

from services.chat import handle_chat
import json

print("=" * 80)
print("MARATHI QUERY TEST")
print("=" * 80)

# Wrap in Flask context
with app.app_context():

    # Test 1: Marathi plant query
    query_mr_plant = "अश्वगंधाबद्दल माहिती द्या"  # Tell me about Ashwagandha
    print(f"\n[TEST 1] Marathi Plant Query")
    print(f"Query: {query_mr_plant}")
    print("-" * 80)
    result = handle_chat(query_mr_plant, session_id="test_mr_1", lang="mr")
    print(f"Language Detected: {result.get('lang', 'NOT SET')}")
    print(f"Answer Length: {len(result['answer'])} characters")
    print(f"Answer Preview:\n{result['answer'][:500]}...")

    # Test 2: Marathi disease query
    query_mr_disease = "मला सर्दी आहे"  # I have a cold
    print(f"\n[TEST 2] Marathi Disease Query")
    print(f"Query: {query_mr_disease}")
    print("-" * 80)
    result = handle_chat(query_mr_disease, session_id="test_mr_2", lang="mr")
    print(f"Language Detected: {result.get('lang', 'NOT SET')}")
    print(f"Answer Length: {len(result['answer'])} characters")
    print(f"Provisional Preps: {len(result.get('provisional', []))}")
    print(f"Answer Preview:\n{result['answer'][:600]}...")

    # Test 3: Compare English vs Marathi same query
    query_en = "I have a cold"
    query_mr = "मला सर्दी आहे"
    print(f"\n[TEST 3] English vs Marathi - Same Query")
    print("-" * 80)
    result_en = handle_chat(query_en, session_id="test_en_cold")
    result_mr = handle_chat(query_mr, session_id="test_mr_cold", lang="mr")
    print(f"English Response Length: {len(result_en['answer'])} chars")
    print(f"Marathi Response Length: {len(result_mr['answer'])} chars")
    print(f"Preps Found (English): {len(result_en.get('provisional', []))}")
    print(f"Preps Found (Marathi): {len(result_mr.get('provisional', []))}")

    # Check if sections are missing in Marathi
    sections = ["preparation", "dosage", "timing", "assessment", "क्षमता", "औषधप्रमाण", "वेळ", "मूल्यांकन"]
    print(f"\nEnglish - Has 'Assessment': {'Assessment' in result_en['answer']}")
    print(f"Marathi - Has 'Assessment': {'Assessment' in result_mr['answer']}")
    print(f"Marathi - Has Marathi 'Assessment': {any(s in result_mr['answer'] for s in sections)}")

    # Show full English response
    print(f"\n[FULL RESPONSE] English (I have a cold):")
    print("-" * 80)
    print(result_en['answer'])

    # Show full Marathi response
    print(f"\n[FULL RESPONSE] Marathi (मला सर्दी आहे):")
    print("-" * 80)
    print(result_mr['answer'])
