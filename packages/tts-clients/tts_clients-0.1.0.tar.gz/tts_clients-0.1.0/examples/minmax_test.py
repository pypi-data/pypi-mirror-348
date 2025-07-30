from dotenv import load_dotenv

from tts_clients.mini_max import MiniMaxT2AClient
from tts_clients.models import TextToAudioRequest, VoiceSetting


load_dotenv()


client = MiniMaxT2AClient()
r = client.text_to_audio(TextToAudioRequest(text="こんにちは！", voice_setting=VoiceSetting(emotion="angry")))
r.data.save("test.mp3")
