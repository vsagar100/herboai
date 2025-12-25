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
        # Use the lighter 200M checkpoints to avoid CPU timeouts/OOM on 1B models.
        model_map = {
            "en-indic": "ai4bharat/indictrans2-en-indic-dist-200M",
            "indic-en": "ai4bharat/indictrans2-indic-en-dist-200M",
          #  "indic-indic": "ai4bharat/indictrans2-indic-indic-dist-320M",
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

# Language code reference
LANGUAGE_CODES = {
    # Language name: (code, script)
    "english": "eng_Latn",
    "hindi": "hin_Deva",
    "marathi": "mar_Deva"
}

# Function to list all supported languages
def get_supported_languages():
    """Return dictionary of supported languages"""
    return LANGUAGE_CODES
