import typer
import pandas as pd
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from audiovisually.preprocess import video_to_mp3, mp3_to_text_assemblyai, translate_df
from audiovisually.predict import classify_emotions, classify_emotions_huggingface

app = typer.Typer(help="Audiovisually CLI - Process and analyze audiovisual files.")

@app.command()
def convert_video(
    video_path: str = typer.Argument(..., help="Path to the input video file"),
    output_path: str = typer.Option(None, help="Path to save the converted MP3 file (optional)"),
):
    """Convert a video file to MP3 audio."""
    audio_path = video_to_mp3(video_path, output_path=output_path)
    typer.echo(f"Audio saved to: {audio_path}")

@app.command()
def transcribe(
    audio_path: str = typer.Argument(..., help="Path to the MP3 audio file"),
    assembly_api_key: str = typer.Option(..., prompt=True, hide_input=True, help="AssemblyAI API key"),
    output_path: str = typer.Option(None, help="Path to save the transcribed CSV file (optional)"),
):
    """Transcribe MP3 audio to text using AssemblyAI."""
    df = mp3_to_text_assemblyai(audio_path, assembly_api_key)
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
    else:
        output_path = audio_path.replace('.mp3', '.csv')
        df.to_csv(output_path, index=False)
    typer.echo(f"Transcription saved to: {output_path}")

@app.command()
def translate(
    input_csv: str = typer.Argument(..., help="CSV file with sentences to translate"),
    output_csv: str = typer.Option(None, help="Where to save the translated CSV"),
    source_lang: str = typer.Option('auto', help="Source language (default: auto)"),
    dest_lang: str = typer.Option('en', help="Destination language (default: English)"),
    text_column: str = typer.Option('Sentence', help="Column name for text to translate (default: 'Sentence')"),
    translated_column: str = typer.Option('Translation', help="Column name for translated text (default: 'Translation')"),
):
    """Translate sentences in a CSV file to English."""
    import pandas as pd
    df = pd.read_csv(input_csv)
    translated_df = translate_df(df)
    if output_csv is None:
        base, ext = os.path.splitext(input_csv)
        output_csv = f"{base}_translated{ext}"
    translated_df.to_csv(output_csv, index=False)
    typer.echo(f"Translated CSV saved to: {output_csv}")

@app.command()
def classify(
    input_csv: str = typer.Argument(..., help="CSV file with sentences to classify"),
    output_csv: str = typer.Option(None, help="Where to save the classified CSV"),
    custom: bool = typer.Option(False, help="Use custom model for classification"),
    model_path: str = typer.Option(None, help="Path to the custom model (if using custom)"),
    huggingface_model: str = typer.Option("j-hartmann/emotion-english-distilroberta-base", help="Hugging Face model name (default: 'j-hartmann/emotion-english-distilroberta-base')"),
):
    """Classify emotions in sentences using a model and save to a new file by default."""
    import pandas as pd
    df = pd.read_csv(input_csv)
    if custom:
        if model_path is None:
            typer.echo("Error: Model path is required when using a custom model.")
            raise typer.Exit(code=1)
        df = classify_emotions(model_path, df)
    else:
        df = classify_emotions_huggingface(df, huggingface_model)

    if output_csv is None:
        base, ext = os.path.splitext(input_csv)
        output_csv = f"{base}_classified{ext}"

    df.to_csv(output_csv, index=False)
    typer.echo(f"Classified emotions saved to: {output_csv}")

if __name__ == "__main__":
    app()