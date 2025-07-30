import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
import pytest
from audiovisually.predict import classify_emotions, classify_emotions_huggingface
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from unittest.mock import patch, MagicMock
import contextlib
import io

## ---------------  (1) Classify emotions with custom model ------------------------------

MODEL_PATH = os.path.join(project_root, 'best_model')
LABEL_MAP = ['anger', 'sadness', 'disgust', 'fear', 'surprise', 'neutral', 'happiness']

# (1) - Preparation: Sample data for testing
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'Sentence': [
            "This is a happy sentence.",
            "I feel very sad today.",
            "That was surprising!",
            "He is full of anger."
        ]
    })

# (1) - Test 1
def test_classify_emotions_returns_dataframe_with_predictions(sample_dataframe):
    result_df = classify_emotions(MODEL_PATH, sample_dataframe.copy())
    assert isinstance(result_df, pd.DataFrame)
    assert 'Predicted Emotion' in result_df.columns
    assert len(result_df) == len(sample_dataframe)
    assert len(result_df['Predicted Emotion']) == len(sample_dataframe['Sentence'])
    predicted_emotions = result_df['Predicted Emotion'].tolist()
    assert all(emotion in LABEL_MAP for emotion in predicted_emotions)

# (1) - Test 2
def test_classify_emotions_handles_empty_and_single_sentence_dataframe():
    # Test with empty DataFrame
    empty_df = pd.DataFrame({'Sentence': []})
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        empty_result_df = classify_emotions(MODEL_PATH, empty_df.copy())
        assert "Warning: Input DataFrame is empty." in stdout.getvalue()
    assert isinstance(empty_result_df, pd.DataFrame)
    assert 'Predicted Emotion' in empty_result_df.columns
    assert len(empty_result_df) == 0

    # Test with single-sentence DataFrame
    single_df = pd.DataFrame({'Sentence': ["Just one sentence here."]})
    single_result_df = classify_emotions(MODEL_PATH, single_df.copy())
    assert isinstance(single_result_df, pd.DataFrame)
    assert 'Predicted Emotion' in single_result_df.columns
    assert len(single_result_df) == 1
    assert single_result_df['Predicted Emotion'].tolist()[0] in LABEL_MAP

    # Test with a DataFrame containing an empty string
    empty_string_df = pd.DataFrame({'Sentence': [""]})
    empty_string_result_df = classify_emotions(MODEL_PATH, empty_string_df.copy())
    assert empty_string_result_df['Predicted Emotion'].tolist()[0] == ''

    # Test with a DataFrame containing a NaN value
    nan_df = pd.DataFrame({'Sentence': [pd.NA]})
    nan_result_df = classify_emotions(MODEL_PATH, nan_df.copy())
    assert nan_result_df['Predicted Emotion'].tolist()[0] == ''

# (1) - Test 3
def test_classify_emotions_loads_specified_model():
    try:
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        assert model is not None
        assert tokenizer is not None
    except Exception as e:
        pytest.fail(f"Failed to load the specified model ({MODEL_PATH}): {e}")

## ---------------  (2) Classify emotions with Hugging Face pipeline ------------------------------

TEST_MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
EXPECTED_LABELS = ['anger', 'sadness', 'disgust', 'fear', 'surprise', 'neutral', 'happiness']

# (2) - Preparation: Sample data for testing
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'Sentence': [
            "This is a happy sentence.",
            "I feel very sad today.",
            "That was surprising!",
            "He is full of anger."
        ]
    })

# (2) - Test 1
def test_classify_emotions_huggingface_returns_dataframe_with_predictions(sample_dataframe):
    result_df = classify_emotions_huggingface(sample_dataframe.copy(), model_name=TEST_MODEL_NAME)
    assert isinstance(result_df, pd.DataFrame)
    assert 'Predicted Emotion' in result_df.columns
    assert len(result_df) == len(sample_dataframe)
    assert len(result_df['Predicted Emotion']) == len(sample_dataframe['Sentence'])
    assert result_df['Predicted Emotion'].tolist()[0] in EXPECTED_LABELS

# (2) - Test 2
def test_classify_emotions_huggingface_handles_empty_and_invalid_model():
    # Test with empty DataFrame
    empty_df = pd.DataFrame({'Sentence': []})
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        empty_result_df = classify_emotions_huggingface(empty_df.copy(), model_name=TEST_MODEL_NAME)
        assert "Warning: Input DataFrame is empty." in stdout.getvalue()
    assert isinstance(empty_result_df, pd.DataFrame)
    assert 'Predicted Emotion' in empty_result_df.columns
    assert len(empty_result_df) == 0

    # Test with an invalid model name
    invalid_model_name = "this-model-does-not-exist"
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        invalid_model_df = pd.DataFrame({'Sentence': ["test sentence"]})
        invalid_result_df = classify_emotions_huggingface(invalid_model_df.copy(), model_name=invalid_model_name)
        assert f"Error loading pipeline with model '{invalid_model_name}'" in stdout.getvalue()
    assert isinstance(invalid_result_df, pd.DataFrame)
    assert 'Predicted Emotion' in invalid_result_df.columns
    assert len(invalid_result_df) == 1
    assert invalid_result_df['Predicted Emotion'].tolist() == ['']

# (2) - Test 3
def test_classify_emotions_huggingface_handles_empty_and_nan_sentences():
    df = pd.DataFrame({'Sentence': ["", pd.NA, "Another sentence"]})
    result_df = classify_emotions_huggingface(df.copy(), model_name=TEST_MODEL_NAME)
    assert len(result_df) == 3
    assert 'Predicted Emotion' in result_df.columns
    assert result_df['Predicted Emotion'].tolist()[0] == ''
    assert result_df['Predicted Emotion'].tolist()[1] == ''
    assert isinstance(result_df['Predicted Emotion'].tolist()[2], str)
    assert result_df['Predicted Emotion'].tolist()[2] in EXPECTED_LABELS
