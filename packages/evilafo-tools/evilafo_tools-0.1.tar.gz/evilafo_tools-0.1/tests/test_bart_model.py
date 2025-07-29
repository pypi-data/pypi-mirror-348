from evilafo_tools.bart_model import BartModel

def test_summarize():
    model = BartModel()
    text = "Hugging Face is a company that provides machine learning models and datasets. It focuses on democratizing AI."
    summary = model.summarize(text)
    assert len(summary) > 0  # Le summary ne doit pas être vide
