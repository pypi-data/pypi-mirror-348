# Evilafo-tools

**Evilafo-tools** est une bibliothèque Python conçue pour faciliter l'utilisation des modèles **BERT** et **BART** de Hugging Face dans des tâches courantes de traitement du langage naturel (NLP), telles que la classification de texte, la génération de résumé et la réponse à des questions.

Cette bibliothèque offre une interface simple et intuitive pour interagir avec les puissants modèles de **Hugging Face**, tout en prenant en charge les principaux cas d'utilisation de NLP.

## Fonctionnalités

* **Classification de texte** avec BERT
* **Réponse à des questions** avec BERT
* **Génération de résumés** avec BART

## Installation

### Prérequis

Avant d'installer **Evilafo-tools**, assure-toi d'avoir **Python 3.6+** et **pip** installés sur ton système.

### Installer depuis PyPI

La façon la plus simple d'installer **Evilafo-tools** est d'utiliser **pip** :

```bash
pip install Evilafo-tools
```

### Installer avec support GPU (optionnel)

Si tu souhaites utiliser la version **GPU** de **PyTorch** pour des performances accrues (notamment pour l’entraînement ou l’inférence sur des modèles de grande taille), tu peux installer les dépendances GPU avec :

```bash
pip install Evilafo-tools[gpu]
```

### Dépendances

**Evilafo-tools** nécessite les bibliothèques suivantes :

* **transformers** : La bibliothèque de Hugging Face pour utiliser BERT, BART et d'autres modèles pré-entrainés.
* **torch** : PyTorch, la bibliothèque de calcul pour le machine learning.
* **numpy** : Manipulation de données numériques.

Si tu choisis l'option GPU, **PyTorch avec CUDA** sera installé pour accélérer les calculs sur un GPU.

## Utilisation

### Exemple de classification de texte avec BERT

Pour utiliser **BERT** pour classifier un texte, tu peux faire comme suit :

```python
from evilafo_tools.bert_model import BertModel

# Charger le modèle BERT pour la classification
model = BertModel()
model.load_for_classification()

# Classifier un texte
text = "I love programming in Python!"
result = model.classify(text)
print(f"Classification result: {result}")
```

### Exemple de réponse à une question avec BERT

Pour utiliser **BERT** pour répondre à des questions à partir d'un texte de contexte :

```python
from evilafo_tools.bert_model import BertModel

# Charger le modèle BERT pour la question-réponse
model = BertModel()
model.load_for_question_answering()

# Définir la question et le contexte
context = "Hugging Face is creating a tool that democratizes AI."
question = "What is Hugging Face creating?"

# Obtenir la réponse
answer = model.answer_question(question, context)
print(f"Answer: {answer}")
```

### Exemple de génération de résumé avec BART

Pour générer un résumé avec **BART** :

```python
from evilafo_tools.bart_model import BartModel

# Charger le modèle BART pour la génération de résumé
model = BartModel()

# Résumer un texte
text = "Hugging Face is a company that provides machine learning models and datasets. It focuses on democratizing AI."
summary = model.summarize(text)
print(f"Summary: {summary}")
```

## Contribution

Les contributions sont les bienvenues ! Si tu veux améliorer cette bibliothèque, corriger des bugs ou ajouter de nouvelles fonctionnalités, n’hésite pas à ouvrir une **pull request** sur le [dépôt GitHub](https://github.com/Evilafo/Evilafo-tools).

### Comment contribuer :

1. Fork le projet.
2. Crée une branche pour ta fonctionnalité ou correction de bug (`git checkout -b feature-xyz`).
3. Apporte tes modifications.
4. Teste tes modifications.
5. Envoie une **pull request** avec une description claire de tes changements.

## Licence

**Evilafo-tools** est distribué sous la licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.


