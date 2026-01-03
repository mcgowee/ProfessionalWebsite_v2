import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load env variables from the same place the app does
load_dotenv()

key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_SPEECH_REGION")

print(f"Testing Azure Speech Credentials...")
print(f"Key: {key[:4]}...{key[-4:] if key else 'None'}")
print(f"Region: {region}")

if not key or not region:
    print("ERROR: Missing Key or Region in .env")
    exit(1)

config = speechsdk.SpeechConfig(subscription=key, region=region)

# Try a simple TTS operation (easier than STT because no mic needed)
# This will verify if the Key/Region allow connection.
synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=None)

print("Attempting connection to Azure...")
result = synthesizer.speak_text_async("Hello world").get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("SUCCESS: Connection established and audio synthesized!")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"FAILURE: Canceled.")
    print(f"Reason: {cancellation_details.reason}")
    print(f"Error Details: {cancellation_details.error_details}")
    print(f"Error Code: {cancellation_details.error_code}")
else:
    print(f"Review Result: {result.reason}")
