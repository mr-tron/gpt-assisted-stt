import io

import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
device = 0

audio = pyaudio.PyAudio()

print("----------------------record device list---------------------")
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    device = i
    name = audio.get_device_info_by_host_api_device_index(0, i).get('name')
    print(i, name)
    if name == 'default':
        break

print("-------------------------------------------------------------")

def record_audio(stop, callback):

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=device,
                        frames_per_buffer=CHUNK)
    print("recording started")
    Recordframes = []

    while stop.is_set() == False:
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print("recording stopped")
    memory_file = io.BytesIO()
    memory_file.name = "test.wav"
    waveFile = wave.open(memory_file, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()
    callback(memory_file)