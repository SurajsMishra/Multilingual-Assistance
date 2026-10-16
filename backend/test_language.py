import sys
from services.language_service import detect_language

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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