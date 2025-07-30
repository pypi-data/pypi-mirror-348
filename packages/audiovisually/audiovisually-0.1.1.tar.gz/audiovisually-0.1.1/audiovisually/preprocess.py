# This file is part of the Audiovisually project.
# Here we can find some preprocessing functions for the video/audio files.
# The current functions are:

# 1. video_to_mp3: Converts a video file to MP3 format.
# 2. mp3_to_text_assemblyai: Transcribes MP3 audio to text using AssemblyAI.
# 3. translate_df: Translates text in a DataFrame from one language to another using a pre-trained translation model.

# Feel free to add any functions you find useful.

import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip
from googletrans import Translator
import tempfile
import whisper
import torch
import os
import sys
import nltk
import asyncio
from googletrans import Translator
from .utils import build_assemblyai_model

#nltk.download('punkt', quiet=True) # Download only if not already present
#nltk.download('punkt_tab', quiet=True) # Download only if not already present

## (1) Video to MP3
def video_to_mp3(video_path, output_path=None):
    """Converts video to MP3 and saves it to the specified output path or the same folder as the input file."""
    try:
        sys.stdout = open(os.devnull, 'w') # Suppress output
        video = VideoFileClip(video_path)
        sys.stdout = sys.__stdout__ # Restore output
        if video.audio is None:
            return f"!(1)! No audio in video file: {video_path}"

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            audio_path = output_path
        else:
            base, ext = os.path.splitext(os.path.basename(video_path))
            audio_path = os.path.join(os.path.dirname(video_path), f"{base}.mp3")

        video.audio.write_audiofile(audio_path, codec='mp3')
        video.audio.close()
        video.close()
        return audio_path
    except Exception as e:
        return f"!(1)! Video to MP3 error: {e}"

## (2) AssemblyAI Transcription
def mp3_to_text_assemblyai(audio_path, api_key):
    """Transcribes MP3 to text using AssemblyAI."""
    try:
        assemblyai_model, config = build_assemblyai_model(api_key)
        transcript = assemblyai_model.transcribe(audio_path, config=config)
        sentences = nltk.tokenize.sent_tokenize(transcript.text)
        df = pd.DataFrame(sentences, columns=["Sentence"])
        return df
    except Exception as e:
        return f"!(2)! AssemblyAI transcription error: {e}"

## (3) Translation to English
def translate_df(df, source_lang='auto', dest_lang='en', text_column='Sentence', translated_column='Translation'):
    try:
        async def translate_single_text(text, translator_instance):
            if pd.isna(text) or text.strip() == "":
                return ""
            try:
                result = await translator_instance.translate(text, src=source_lang, dest=dest_lang)
                return result.text
            except Exception as inner_e:
                return f"Translation error: {inner_e}"

        async def process_dataframe(dataframe):
            async with Translator() as translator:
                translations = []
                for text in dataframe[text_column]:
                    translations.append(await translate_single_text(text, translator))
                return translations

        df[translated_column] = asyncio.run(process_dataframe(df))
        return df
    except Exception as e:
        return f"!(3) Translation error: {e}"
