from faster_whisper import WhisperModel
import os

MODEL_SIZE = "tiny"

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_path: str):

    print("\n==============================")
    print("WHISPER DEBUG")
    print("==============================")

    print("Audio path:", audio_path)
    print("File exists:", os.path.exists(audio_path))

    if os.path.exists(audio_path):
        print(
            "File size:",
            os.path.getsize(audio_path),
            "bytes"
        )

    print("Starting Whisper...")

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=False
    )

    print("Detected language:", info.language)
    print("Language probability:", info.language_probability)

    text_parts = []

    for segment in segments:

        print(
            "SEGMENT:",
            segment.start,
            "->",
            segment.end,
            "|",
            repr(segment.text)
        )

        text_parts.append(segment.text)

    text = " ".join(text_parts).strip()

    print("FINAL TRANSCRIPTION:", repr(text))
    print("==============================\n")

    return {
        "text": text,
        "language": info.language
    }