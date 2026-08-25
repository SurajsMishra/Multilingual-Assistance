import edge_tts
VOICE_MAP = {
    "hi": "hi-IN-SwaraNeural",
    "en": "en-IN-NeerjaNeural",
    "bn": "bn-IN-TanishaaNeural",
    "ta": "ta-IN-PallaviNeural",
    "te": "te-IN-ShrutiNeural",
    "mr": "mr-IN-AarohiNeural",
    "gu": "gu-IN-DhwaniNeural"
}
async def text_to_speech(
    text: str,
    language: str,
    output_path : str
):
    voice = VOICE_MAP.get(
        language, "en-IN-NeerjaNeural"
    )
    communicate = edge_tts.Communicate(
        text, voice
    )
    await communicate.save(output_path)
    return output_path

