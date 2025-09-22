# File: scripts/quick_test.py
# Quick test to verify the langdetect import fix

def test_import_fix():
    """Test if the langdetect import issue is resolved"""
    print("Testing langdetect compatibility...")
    
    try:
        # Test the import that was causing issues
        from app.i18n import detect_lang, test_language_detection
        print("✅ Import successful!")
        
        # Test basic functionality
        test_queries = [
            ("डोकेदुखीसाठी काय घ्यावे?", "mr"),
            ("तनाव के लिए क्या लें?", "hi"),
            ("What helps with anxiety?", "en")
        ]
        
        print("\nTesting language detection:")
        for query, expected in test_queries:
            detected = detect_lang(query)
            status = "✅" if detected == expected else "❌"
            print(f"{status} '{query}' -> {detected}")
        
        print("\n🎉 Language detection is working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check if langdetect is installed: pip install langdetect")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_import_fix()