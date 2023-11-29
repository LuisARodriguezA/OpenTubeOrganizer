import pandas as pd
from tabulate import tabulate
from bs4 import BeautifulSoup
import requests
from pytube import YouTube

def get_latest_video_statistics(channel_link):
    try:
        # Get the HTML content of the channel page
        response = requests.get(channel_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the link to the latest video on the channel page using a more specific CSS selector
        latest_video_link = soup.select_one('a#video-title')
        
        if latest_video_link is None:
            print(f"No se pudo encontrar el enlace al último video para el canal: {channel_link}")
            return None
        
        video_url = f'https://www.youtube.com{latest_video_link["href"]}'

        # Get video details using PyTube
        yt_video = YouTube(video_url)
        stats = {
            'Nombre del canal': yt_video.author,
            'Título del último video': yt_video.title,
            'Vistas del último video': yt_video.views,
            'Likes del último video': yt_video.likes,
            'Dislikes del último video': yt_video.dislikes,
        }
        return stats
    except Exception as e:
        print(f"Error al obtener estadísticas del último video: {str(e)}")
        return None

get_latest_video_statistics("https://www.youtube.com/@melvinthinks")