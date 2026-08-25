from services.speech_service import speech_to_text
result = speech_to_text("text_audio.wav")
print("Text:", result["text"] )
print("Language: " , result["language"])