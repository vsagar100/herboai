from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

class LocalSummarizer:
    def __init__(self, model_name="t5-small"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def summarize(self, text: str, max_length=60) -> str:
        """Generate short, human-readable summaries locally"""
        if not text.strip():
            return ""
        input_text = f"summarize: {text}"
        inputs = self.tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        summary_ids = self.model.generate(
            inputs,
            max_length=max_length,
            min_length=10,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
