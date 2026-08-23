from langdetect import detect, LangDetectException

SUPPORTED_LANGUAGE = {
    "en": "English",
    "hi": "Hindi",
    "ur": "Urdu",
    "bn": "Bengali",
    "te": "Telugu",
    "mr": "Marathi",
    "ta": "Tamil",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "or": "Odia",
    "pa": "Punjabi",
}

def detect_language(text:str):
    try:
        language_code = detect(text)
        if language_code in SUPPORTED_LANGUAGE:
            return language_code
        return "en"
    except LangDetectException:
        return "en"