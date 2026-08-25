from faster_whisper import WhisperModel
MODEL_SIZE = "tiny"
model = WhisperModel(
    MODEL_SIZE,
    device = "cpu",
    compute_type = "int8"
)
def speech_to_text(audio_path: str) -> str:
    segments, info = model.transcribe(
        audio_path,
        beam_size = 5
    )
    text = ""
    for segment in segments:
        text += segment.text

    return {
        "text": text.strip(),
        "language": info.language
    }