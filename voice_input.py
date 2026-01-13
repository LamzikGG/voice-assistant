import json
import os
from function.times import get_day
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
import sounddevice as sd

load_dotenv()

model = Model(os.getenv("url_model"))
rec = KaldiRecognizer(model, 16000) #Частота дискретизации для распознавания голоса


def callback(indata, frames, time, status): 
    if status:
        print(status)
    # Для RawInputStream преобразуем напрямую
    if rec.AcceptWaveform(bytes(indata)):
        text = json.loads(rec.Result())
        result = text.get("text", "").lower()
        if result:
            if os.path.exists('phrase.json'): #Добавляю условние для искоринение обновление одного "списка"
                with open('phrase.json', 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        if isinstance(data, dict): # У меня записывается как один объект и идет как список 
                            data = [data]
                        elif not isinstance(data, list):
                            data = []
                    except json.JSONDecodeError:
                        data = []
            else: 
                data = []
            new_entry = { 
                "time_phrase": get_day(),
                "phrase": result
            }
            data.append(new_entry)
            with open('phrase.json', 'w', encoding='utf-8') as f:
                json.dump(data, f ,ensure_ascii=False, indent=2)

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Запись")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("Остановка")
