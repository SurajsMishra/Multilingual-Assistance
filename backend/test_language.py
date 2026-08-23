from services.language_service import detect_language
texts = [
    "There is no water supply in my area.",
    "मेरे इलाके में पानी नहीं आ रहा है।",
    "আমাদের এলাকায় পানি নেই।",
    "எங்கள் பகுதியில் தண்ணீர் இல்லை."
]

for text in texts:
    language = detect_language(text)
    print("Text:", text)
    print("Language:", language)
    print("----------")