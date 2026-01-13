from datetime import datetime

def get_time() -> str: # Для вывода времени с голосового сообщения
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def get_day() -> str: #Для хранения информации
    day = datetime.now()
    return day.strftime("%d-%m-%Y, %H:%M:%S")
