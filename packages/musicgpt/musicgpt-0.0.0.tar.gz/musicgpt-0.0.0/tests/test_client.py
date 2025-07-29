from musicgpt import MusicGPTClient
from configparser import ConfigParser

config = ConfigParser()
config.read('tests/config.ini')
api_key = config.get('musicgpt', 'api_key')
client = MusicGPTClient(api_key=api_key)

resp = client.music_ai(prompt="create song about manchester united")
print(f"Task ID: {resp.task_id} Task Status: {resp.task_status} ETA: {resp.eta} seconds")
doc = client.wait_for_completion(resp.task_id, conversion_type=resp.conversion_type, verbose=1)
print(doc)


resp = client.voice_changer(
    audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    voice_id="Drake",
    remove_background=False
)

print(f"Task ID: {resp.task_id} Task Status: {resp.task_status} ETA: {resp.eta} seconds")
doc = client.wait_for_completion(resp.task_id, conversion_type=resp.conversion_type, verbose=1)
print(doc)

resp = client.cover(
    audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", 
    voice_id="Drake",
)

print(f"Task ID: {resp.task_id} Task Status: {resp.task_status} ETA: {resp.eta} seconds")
doc = client.wait_for_completion(resp.task_id, conversion_type=resp.conversion_type, verbose=1)
print(doc)

resp = client.text_to_speech(
    text="Hello, this is a test of the MusicGPT text to speech feature.",
    voice_id="Drake"
    )
print(f"Task ID: {resp.task_id} Task Status: {resp.task_status} ETA: {resp.eta} seconds")
doc = client.wait_for_completion(resp.task_id, conversion_type=resp.conversion_type, verbose=1)
print(doc)