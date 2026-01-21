from googleapiclient.discovery import build
import webbrowser
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("youtube_api")

def search_and_play_youtube_video(query, api_key):
    """"
    запрос -> поиск видео -> преобразование в mp3 -> проигрывать пользователю
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Выполняем поиск
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=1,
        order='relevance'
    ).execute()
    
    if not search_response['items']:
        print("Видео не найдено")
        return None
    
    # перове видео из поиска
    video_id = search_response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # открываем браузер
    webbrowser.open(video_url)
    
    return video_url