#requires the installation of --upgrade google-cloud-speech

from google.cloud import speech
import wave
import audioop

client = speech.SpeechClient.from_service_account_file('key.json')

def transcribe(file_name):
    with wave.open(file_name, mode='rb') as fd:
        frames = fd.readframes(1000000) # 1 million frames max
    
    audio_file = speech.RecognitionAudio(content=frames)
    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        audio_channel_count=1,
        encoding="LINEAR16",
        language_code='fil-PH',
    )

    response = client.recognize(
        config=config,
        audio=audio_file
    )
    print("Recorded Text: {}".format(response.results[0].alternatives[0].transcript))
    return response.results[0].alternatives[0].transcript