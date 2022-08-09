import subprocess
from gtts import gTTS


def create_default_sound_files():
    # Create the I'm listening sound file
    tts = gTTS(text="Yes?", lang="en", slow=False)
    tts.save("listening.mp3")


def play_audio_response(text, filename="response.mp3"):
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(filename)
    subprocess.check_output(["mpg123", "-q", filename])
