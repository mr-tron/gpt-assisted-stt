
from openai import OpenAI

openai_client = OpenAI(api_key="")

# for speech-to-text
GLOSSARY = "TONAPI, TON, nanoTON, TONs"
try:
    GLOSSARY = open("glossary.txt").read()
except:
    pass

# for text post-proccessing
PROMPT = "You are text corrector. Your task is to correct a text that contains both Russian and English elements. Carefully review and correct syntactical errors and voice recognition mistakes in the Russian parts of the text. For the English segments, in addition to syntactical errors and typos, also focus on style and sentence structure to ensure the text is clear, logical, and well-structured."


def transcript(audio_file):
    transcription = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        prompt="Glossary: " + GLOSSARY
    )
    print(transcription.text)
    return transcription.text


def post_proccess(transcript):
    return openai_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": transcript,
            }
        ],
        model="gpt-4-turbo-preview",
        stream=True,
    )