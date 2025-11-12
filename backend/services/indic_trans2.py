import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re

class IndicTranslator:
    def __init__(self, direction="en-indic"):
        """
        Initialize the translator
        direction options:
        - "en-indic": English to Indian languages
        - "indic-en": Indian languages to English
        - "indic-indic": Indian to Indian languages
        """
        model_map = {
            "en-indic": "ai4bharat/indictrans2-en-indic-1B",
            "indic-en": "ai4bharat/indictrans2-indic-en-1B",
            "indic-indic": "ai4bharat/indictrans2-indic-indic-1B"
        }
        
        model_name = model_map[direction]
        print(f"Loading model: {model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
        
        # Move to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print(f"Model loaded on: {self.device}")
        
    def preprocess_text(self, text, src_lang, tgt_lang):
        """IndicTrans2 expects literal 'src_lang tgt_lang sentence' format."""
        return f"{src_lang} {tgt_lang} {text.strip()}"
    
    def postprocess_text(self, text):
        """Clean up the translated text"""
        # Remove any language tags that might be in output
        text = re.sub(r'^[a-z]{3}_[A-Z][a-z]+:\s*', '', text)
        return text.strip()
        
    def translate(self, sentences, src_lang, tgt_lang):
        """
        Translate sentences from source to target language
        
        Args:
            sentences: string or list of strings
            src_lang: source language code
            tgt_lang: target language code
        
        Language codes:
        eng_Latn (English), hin_Deva (Hindi), ben_Beng (Bengali), 
        guj_Gujr (Gujarati), mar_Deva (Marathi), tam_Taml (Tamil),
        tel_Telu (Telugu), kan_Knda (Kannada), mal_Mlym (Malayalam),
        pan_Guru (Punjabi), ory_Orya (Odia), asm_Beng (Assamese)
        """
        # Convert single sentence to list
        if isinstance(sentences, str):
            sentences = [sentences]
            single_input = True
        else:
            single_input = False
        
        # Preprocess
        processed_sentences = [self.preprocess_text(s, src_lang, tgt_lang) for s in sentences]

        # Tokenize
        inputs = self.tokenizer(
            processed_sentences,
            truncation=True,
            padding="longest",
            return_tensors="pt",
            max_length=256
        ).to(self.device)

        # Determine BOS token for decoder
        tgt_lang_token = self.tokenizer.convert_tokens_to_ids(tgt_lang)
        if tgt_lang_token is None and hasattr(self.tokenizer, "lang_code_to_id"):
            tgt_lang_token = self.tokenizer.lang_code_to_id.get(tgt_lang)
        if tgt_lang_token is None:
            raise ValueError(f"Unknown target language code: {tgt_lang}")
        
        # Generate translations
        with torch.no_grad():
            generated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=tgt_lang_token,
                min_length=0,
                max_length=256,
                num_beams=5,
                num_return_sequences=1
            )
        
        # Decode
        translations = self.tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
        
        # Postprocess
        translations = [self.postprocess_text(t) for t in translations]
        
        # Return single string if input was single string
        return translations[0] if single_input else translations


# Example usage
if __name__ == "__main__":
    # Initialize translator for English to Indic languages
    print("Initializing translator...")
    translator = IndicTranslator(direction="en-indic")
    print()
    
    # Example 1: Single sentence translation (English to Hindi)
    print("=" * 60)
    print("Example 1: English to Hindi")
    print("=" * 60)
    english_text = "Hello, how are you?"
    hindi_translation = translator.translate(
        sentences=english_text,
        src_lang="eng_Latn",
        tgt_lang="hin_Deva"
    )
    print(f"English: {english_text}")
    print(f"Hindi: {hindi_translation}")
    print()
    
    # Example 2: English to Marathi
    print("=" * 60)
    print("Example 2: English to Marathi")
    print("=" * 60)
    english_text = "Thank you for your help."
    marathi_translation = translator.translate(
        sentences=english_text,
        src_lang="eng_Latn",
        tgt_lang="mar_Deva"
    )
    print(f"English: {english_text}")
    print(f"Marathi: {marathi_translation}")
    print()
    
    # Example 3: Batch translation (English to Tamil)
    print("=" * 60)
    print("Example 3: Batch Translation (English to Tamil)")
    print("=" * 60)
    texts = [
        "Good morning",
        "What is your name?",
        "I am learning Indian languages"
    ]
    
    tamil_translations = translator.translate(
        sentences=texts,
        src_lang="eng_Latn",
        tgt_lang="tam_Taml"
    )
    
    for eng, tam in zip(texts, tamil_translations):
        print(f"  EN: {eng}")
        print(f"  TA: {tam}")
        print()
    
    # Example 4: English to multiple languages
    print("=" * 60)
    print("Example 4: One sentence to multiple languages")
    print("=" * 60)
    text = "Welcome to India"
    languages = [
        ("hin_Deva", "Hindi"),
        ("guj_Gujr", "Gujarati"),
        ("tel_Telu", "Telugu"),
        ("kan_Knda", "Kannada")
    ]
    
    print(f"English: {text}\n")
    for lang_code, lang_name in languages:
        translation = translator.translate(text, "eng_Latn", lang_code)
        print(f"{lang_name:12s}: {translation}")
    
    # Example 5: Longer text
    print()
    print("=" * 60)
    print("Example 5: Longer text (English to Hindi)")
    print("=" * 60)
    long_text = "India is a diverse country with many languages and cultures. The people are very friendly and welcoming."
    hindi_long = translator.translate(long_text, "eng_Latn", "hin_Deva")
    print(f"English: {long_text}")
    print(f"Hindi: {hindi_long}")


# Language code reference
LANGUAGE_CODES = {
    # Language name: (code, script)
    "english": "eng_Latn",
    "hindi": "hin_Deva",
    "bengali": "ben_Beng",
    "gujarati": "guj_Gujr",
    "marathi": "mar_Deva",
    "tamil": "tam_Taml",
    "telugu": "tel_Telu",
    "kannada": "kan_Knda",
    "malayalam": "mal_Mlym",
    "punjabi": "pan_Guru",
    "odia": "ory_Orya",
    "assamese": "asm_Beng",
    "sanskrit": "san_Deva"
}

# Function to list all supported languages
def get_supported_languages():
    """Return dictionary of supported languages"""
    return LANGUAGE_CODES
