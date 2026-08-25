import asyncio
from services.tts_service import text_to_speech
async def main():
    output_file = "test_response_hindi.mp3"
    await text_to_speech(
        "आपकी शिकायत सफलतापूर्वक दर्ज कर ली गई है।",
        "hi",
        output_file
    )
    print("Audio created:", output_file)

if __name__ == "__main__":
    asyncio.run(main())