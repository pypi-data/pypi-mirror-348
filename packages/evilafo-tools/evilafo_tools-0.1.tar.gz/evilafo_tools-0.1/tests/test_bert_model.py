from evilafo_tools.bert_model import BertModel

def test_classification():
    model = BertModel()
    model.load_for_classification()
    result = model.classify("I love Python!")
    assert result == 1  # En fonction de ton modèle, le résultat doit être correct

def test_question_answering():
    model = BertModel()
    model.load_for_question_answering()
    answer = model.answer_question("What is Hugging Face?", "Hugging Face is creating a tool that democratizes AI.")
    assert answer == "a tool that democratizes AI"
