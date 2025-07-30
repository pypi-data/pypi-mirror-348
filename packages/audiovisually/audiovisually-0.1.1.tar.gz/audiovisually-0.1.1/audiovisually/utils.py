# This file is part of the Audiovisually project.
# Here we can find mainly utility functions to help us with the project.
# The goal here is to have more flexible functions here that can be used in different parts of the project.
# The current functions are:

# 1. build_assemblyai_model: Builds AssemblyAI model.

# Feel free to add any functions you find useful.

import assemblyai as aai
import pandas as pd
import time
import sys

## (1)
def build_assemblyai_model(api_key):
    """Builds AssemblyAI model."""
    try:
        aai.settings.api_key = api_key
        aai.settings.base_url = "https://api.eu.assemblyai.com"
        assemblyai_model = aai.Transcriber()
        config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.universal,
            language_detection=True
        )
        return assemblyai_model, config
    except Exception as e:
        return f"!(1)! AssemblyAI model error: {e}"


# get_video_duration, get_audio_duration, get_video_fps, get_video_resolution
