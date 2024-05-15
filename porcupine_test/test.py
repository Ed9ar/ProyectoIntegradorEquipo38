import os
import struct
import pyaudio
import pvporcupine
from datetime import datetime

porcupine = None
pa = None
audio_stream = None

def main():
    try:
        porcupine = pvporcupine.create(access_key=os.environ['PORCUPINE_ACCESS_KEY'],
                                    keyword_paths=['.Hola-te-bot_es_mac_v3_0_0.ppn'],
                                    model_path='./porcupine_params_es.pv',
                                    sensitivities=[0.9])

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        print(f"{datetime.now()} - Listening!")
        
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print(f"{datetime.now()} - 'Hola TecBot' detectado")
    except KeyboardInterrupt:
        print(f"{datetime.now()} - Stopped listening!")
        exit()
    except Exception as e:
        exit()
    finally:
        porcupine.delete()

if __name__ == '__main__':
    main()
