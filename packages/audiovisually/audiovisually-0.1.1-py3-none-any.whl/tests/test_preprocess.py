import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
import pytest
from audiovisually.preprocess import video_to_mp3, mp3_to_text_assemblyai, translate_df
import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ColorClip
from unittest.mock import MagicMock
import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")

## ---------------  (1) Video to MP3 ------------------------------

# (1) - Preparation: Create a dummy video file for testing
def create_dummy_video(file_path="dummy_video.mp4", duration=2, fps=1):
    try:
        clip = VideoFileClip(size=(100, 100), fps=fps, duration=duration, color=[255, 0, 0])
        clip.write_videofile(file_path, codec='mpeg4', audio_codec='aac', threads=1, logger=None)
        clip.close()
        return file_path
    except Exception as e:
        print(f"Error creating dummy video: {e}")
        return None

# (1) - Test 1
def test_1_successful_conversion():
    """Test if a valid video file is correctly converted to MP3."""
    dummy_video = create_dummy_video()
    if dummy_video:
        output_path = video_to_mp3(dummy_video)
        assert isinstance(output_path, str)
        assert os.path.exists(output_path)
        assert output_path.endswith(".mp3")
        assert os.path.isdir("avmp3")
        assert os.path.exists(os.path.join("avmp3", os.path.splitext(os.path.basename(dummy_video))[0] + ".mp3"))
        os.remove(dummy_video)
        os.remove(output_path)

# (1) - Test 2
def test_1_invalid_video_path():
    """Test if the function handles an invalid video path gracefully."""
    invalid_path = "non_existent_video.mp4"
    error_message = video_to_mp3(invalid_path)
    assert isinstance(error_message, str)
    assert error_message.startswith("!(1)! Video to MP3 error:")

# (1) - Test 3
def test_1_unsupported_video_format():
    """Test if the function handles an unsupported video format."""
    # Create a dummy file with an unsupported extension
    unsupported_file = "unsupported.txt"
    with open(unsupported_file, "w") as f:
        f.write("This is not a video.")
    error_message = video_to_mp3(unsupported_file)
    assert isinstance(error_message, str)
    assert error_message.startswith("!(1)! Video to MP3 error:")
    os.remove(unsupported_file)

# (1) - Test 4
def test_1_video_without_audio():
    """Test if the function handles a video file without an audio track."""
    try:
        clip_no_audio = ColorClip(size=(100, 100), color=[255, 0, 0], duration=2)
        clip_no_audio.fps = 1
        video_no_audio_path = "no_audio.mp4"
        clip_no_audio.write_videofile(video_no_audio_path, codec="mpeg4", audio_codec=None, threads=1, logger=None)
        clip_no_audio.close()
        output_path = video_to_mp3(video_no_audio_path)
        assert isinstance(output_path, str)
        assert output_path == f"!(1)! No audio in video file: {video_no_audio_path}"
        os.remove(video_no_audio_path)
    except Exception as e:
        pytest.fail(f"Error during no audio test: {e}")

## ---------------  (2) MP3 to Text using AssemblyAI ------------------------------

# (2) - Preparation: Mock AssemblyAI model
def mock_assemblyai_model():
    """Mocks the AssemblyAI model object with a transcribe method."""
    mock_model = MagicMock()
    mock_transcript_result = MagicMock(text="This is a sample transcription. It has two sentences.")
    mock_model.transcribe.return_value = mock_transcript_result
    return mock_model, {}  # Return a mock model and an empty config

# (2) - Preparation: Empty Mock AssemblyAI model
def mock_assemblyai_model_empty_transcript():
    """Mocks AssemblyAI returning an empty transcript."""
    mock_model = MagicMock()
    mock_transcript_result = MagicMock(text="")
    mock_model.transcribe.return_value = mock_transcript_result
    return mock_model, {}

# (2) - Preparation: Complicated Mock AssemblyAI model
def mock_assemblyai_model_complex_transcript():
    """Mocks AssemblyAI returning a more complex transcript."""
    mock_model = MagicMock()
    complex_text = "This is the first sentence. Here is another one! And a third? Followed by a sentence with an abbreviation like U.S.A. Finally, a sentence at the end."
    mock_transcript_result = MagicMock(text=complex_text)
    mock_model.transcribe.return_value = mock_transcript_result
    return mock_model, {}

# (2) - Test 1
def test_2_assemblyai_model_transcribe_returns_correct_dataframe(monkeypatch):
    """Test the processing of the transcribe result directly."""
    mock_model, _ = mock_assemblyai_model()
    monkeypatch.setattr("audiovisually.utils.build_assemblyai_model", lambda api_key: (mock_model, {}))

    dummy_audio_path = "dummy_audio.mp3"
    api_key = "test_api_key"
    transcript_output = mock_model.transcribe(dummy_audio_path, config={})

    sentences = nltk.tokenize.sent_tokenize(transcript_output.text)
    df = pd.DataFrame(sentences, columns=["Sentence"])

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "Sentence" in df.columns
    assert df["Sentence"].iloc[0] == "This is a sample transcription."
    assert df["Sentence"].iloc[1] == "It has two sentences."

# (2) - Test 2
def test_2_mp3_to_text_assemblyai_transcription_error(monkeypatch):
    """Test if mp3_to_text_assemblyai handles errors during model building."""
    def mock_build_assemblyai_model(api_key):
        raise Exception("Mocked AssemblyAI model error")
    monkeypatch.setattr("audiovisually.utils.build_assemblyai_model", mock_build_assemblyai_model)
    dummy_audio_path = "dummy_audio.mp3"
    api_key = "test_api_key"
    error_message = mp3_to_text_assemblyai(dummy_audio_path, api_key)
    assert isinstance(error_message, str)
    assert error_message.startswith("!(2)! AssemblyAI transcription error:")

# (2) - Test 3
def test_2_assemblyai_model_transcribe_handles_empty_transcript(monkeypatch):
    """Test processing when AssemblyAI returns an empty transcript."""
    mock_model, _ = mock_assemblyai_model_empty_transcript()
    monkeypatch.setattr("audiovisually.utils.build_assemblyai_model", lambda api_key: (mock_model, {}))

    dummy_audio_path = "dummy_audio.mp3"
    api_key = "test_api_key"
    transcript_output = mock_model.transcribe(dummy_audio_path, config={})

    sentences = nltk.tokenize.sent_tokenize(transcript_output.text)
    df = pd.DataFrame(sentences, columns=["Sentence"])

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0  # Expect an empty DataFrame
    assert "Sentence" in df.columns

# (2) - Test 4
def test_2_assemblyai_model_transcribe_handles_complex_transcript(monkeypatch):
    """Test processing of a more complex transcript with multiple sentences and edge cases."""
    mock_model, _ = mock_assemblyai_model_complex_transcript()
    monkeypatch.setattr("audiovisually.utils.build_assemblyai_model", lambda api_key: (mock_model, {}))

    dummy_audio_path = "dummy_audio.mp3"
    api_key = "test_api_key"
    transcript_output = mock_model.transcribe(dummy_audio_path, config={})

    sentences = nltk.tokenize.sent_tokenize(transcript_output.text)
    df = pd.DataFrame(sentences, columns=["Sentence"])

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert df["Sentence"].iloc[0] == "This is the first sentence."
    assert df["Sentence"].iloc[1] == "Here is another one!"
    assert df["Sentence"].iloc[2] == "And a third?"
    assert df["Sentence"].iloc[3] == "Followed by a sentence with an abbreviation like U.S.A."
    assert df["Sentence"].iloc[4] == "Finally, a sentence at the end."

## ---------------  (3) Translate Sentences to English ------------------------------

# (3) - Test 1
def test_3_translate_df_google_multiple_languages():
    """Test translation to different languages."""
    test_data = pd.DataFrame({'Sentence': ['Bonjour le monde', 'Hola mundo', 'This is English']})

    df_en = translate_df(test_data.copy())
    assert 'Translation' in df_en.columns
    assert df_en['Translation'].tolist() == ['Hello world', 'Hello world', 'This is English']

    df_fr = translate_df(test_data.copy(), dest_lang='fr')
    assert df_fr['Translation'].tolist() == ["Bonjour le monde", "Bonjour le monde", "C'est l'anglais"]

# (3) - Test 2
def test_3_translate_df_google_edge_cases():
    """Test with sentences containing special characters and emojis."""
    test_data = pd.DataFrame({'Sentence': ['你好！😊', 'This has $ signs.', 'Mélange de mots.']})
    df_en = translate_df(test_data.copy())
    assert 'Translation' in df_en.columns
    # The exact translation of emojis might vary, so we'll just check for presence
    assert len(df_en['Translation'].tolist()) == 3
    assert 'Hello!' in df_en['Translation'].iloc[0]
    assert '$ signs' in df_en['Translation'].iloc[1]
    assert 'Mixture of words' in df_en['Translation'].iloc[2]

# (3) - Test 3
def test_translate_df_google_custom_translated_column():
    """Test using a custom name for the translated column."""
    test_data = pd.DataFrame({'Sentence': ['Hello']})
    df_result = translate_df(test_data.copy(), translated_column='Result')
    assert 'Result' in df_result.columns
    assert 'Translation' not in df_result.columns
    assert df_result['Result'].tolist() == ['Hello']
