import json
import os
from function.times import get_day
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
import sounddevice as sd
import platform
from function.open_music import search_and_play_youtube_video

load_dotenv()

model = Model(os.getenv("url_model"))
youtube_api = os.getenv("youtube_api")
rec = KaldiRecognizer(model, 16000) #Частота дискретизации для распознавания голоса

song_plaing = True
running = True 

def callback(indata, frames, time, status): # Обработка аудиопотока
    global running
    global song_plaing
    if status:
        print(status)
    # Для RawInputStream преобразуем напрямую
    if rec.AcceptWaveform(bytes(indata)):
        text = json.loads(rec.Result())
        result = text.get("text", "").lower()
        print(result)
        if result and any(stop_word in result for stop_word in ["стоп", "отсановись", "заткнись"]):
            running = False
            return
        if result in "включи музыку":
            song_plaing = True
            return
        elif song_plaing:
            song_plaing = False
            if result:       
                return search_and_play_youtube_video(result, youtube_api)

def main():
    global running
    while running:  # Бесконечный цикл для перезапуска
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                            channels=1, callback=callback):
            try:
                while running:
                    sd.sleep(100)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()