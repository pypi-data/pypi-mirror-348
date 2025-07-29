import torch
from transformers import BertTokenizer, BertForSequenceClassification, BertForQuestionAnswering
from torch import nn

class BertModel:
    def __init__(self, model_name='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = None

    def load_for_classification(self):
        """Charge le modèle BERT pour la classification de texte"""
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        self.model.eval()  # Mise en mode évaluation

    def classify(self, text):
        """Classifie un texte donné"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        prediction = torch.argmax(logits, dim=-1).item()
        return prediction

    def load_for_question_answering(self):
        """Charge le modèle BERT pour la question-réponse"""
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.model.eval()

    def answer_question(self, question, context):
        """Répond à une question en utilisant un passage de texte comme contexte"""
        inputs = self.tokenizer.encode_plus(question, context, return_tensors="pt", add_special_tokens=True)
        start_scores, end_scores = self.model(**inputs).values()

        # Trouver les indices du début et de la fin de la réponse
        start_index = torch.argmax(start_scores)
        end_index = torch.argmax(end_scores)
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index + 1])
        )
        return answer
