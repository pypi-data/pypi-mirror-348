# This file is part of the Audiovisually project.
# Here we can find some prediction functions to make our model(s) work.
# The current functions are:

# 1. classify_emotions: Classifies emotions in text using an emotion classification model.

# Feel free to add any functions you find useful.

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification
from transformers import pipeline

## (1) Classify emotions with custom model
def classify_emotions(model_path, df):
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    label_map = ['anger', 'sadness', 'disgust', 'fear', 'surprise', 'neutral', 'happiness']

    if df.empty:
        print("Warning: Input DataFrame is empty. Returning an empty DataFrame with 'Predicted Emotion' column.")
        df['Predicted Emotion'] = []
        return df

    sentences = df['Sentence'].tolist()
    predicted_emotions = [''] * len(sentences)  # initialize with empty strings

    # Filter out non-empty sentences for processing
    non_empty_indices = [i for i, sentence in enumerate(sentences) if pd.notna(sentence) and sentence.strip()]
    non_empty_sentences = [sentences[i] for i in non_empty_indices]

    if non_empty_sentences:
        inputs = tokenizer(non_empty_sentences, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        predicted_ids = outputs.logits.argmax(dim=1).tolist()
        predicted_labels = [label_map[idx] for idx in predicted_ids]

        # Assign predicted labels back to the correct positions
        for i, label in enumerate(predicted_labels):
            predicted_emotions[non_empty_indices[i]] = label

    df['Predicted Emotion'] = predicted_emotions
    return df

## (2) Classify emotions with Hugging Face pipeline
def classify_emotions_huggingface(df, model_name="j-hartmann/emotion-english-distilroberta-base"):
    try:
        classifier = pipeline("text-classification", model=model_name, top_k=None)
    except Exception as e:
        print(f"Error loading pipeline with model '{model_name}': {e}")
        df['Predicted Emotion'] = [''] * len(df)
        return df

    if df.empty:
        print("Warning: Input DataFrame is empty. Returning an empty DataFrame with 'Predicted Emotion' column.")
        df['Predicted Emotion'] = []
        return df

    sentences = df['Sentence'].tolist()
    predicted_emotions = [''] * len(sentences)

    non_empty_indices = [i for i, sentence in enumerate(sentences) if pd.notna(sentence) and sentence.strip()]
    non_empty_sentences = [sentences[i] for i in non_empty_indices]

    if non_empty_sentences:
        try:
            predictions = classifier(non_empty_sentences)
            predicted_labels = [pred[0]['label'] for pred in predictions] # assuming top_k=None returns a list of lists, each with one dict
            for i, label in enumerate(predicted_labels):
                predicted_emotions[non_empty_indices[i]] = label
        except Exception as e:
            print(f"Error during classification: {e}")
            # If an error occurs during classification, the corresponding
            # 'Predicted Emotion' will remain an empty string.

    df['Predicted Emotion'] = predicted_emotions
    df['Predicted Emotion'] = df['Predicted Emotion'].replace('joy', 'happiness')
    return df
