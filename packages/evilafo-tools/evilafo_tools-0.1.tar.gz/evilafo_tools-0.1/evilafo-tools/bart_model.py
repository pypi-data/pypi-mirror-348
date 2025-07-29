from transformers import BartTokenizer, BartForConditionalGeneration

class BartModel:
    def __init__(self, model_name='facebook/bart-large-cnn'):
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.model.eval()  # Mise en mode évaluation

    def summarize(self, text):
        """Génère un résumé à partir d'un texte"""
        inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
        with torch.no_grad():
            summary_ids = self.model.generate(inputs['input_ids'], max_length=150, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
