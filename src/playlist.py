import os

import isodate
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    """Класс который получает id плейлиста и возвращает ссылку на видео с наибольшим колличеством лайков
     и возвращает общее время всех видео плейлиста"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails, snippet',
                                                                 maxResults=50,
                                                                 ).execute()      # отсюда беру id канала для получения имя плейлиста

        channel_id = self.playlist_videos["items"][0]["snippet"]["channelId"]
        playlists = self.youtube.playlists().list(channelId=channel_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.title = playlists["items"][0]["snippet"]["title"]  # имя плейлиста
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    @property
    def total_duration(self):
        """Возвращает общую продолжительность всех видео плейлиста"""

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(video_ids)
                                                         ).execute()
        dt = timedelta(minutes=0, seconds=0)
        for i in video_response["items"]:
            iso_8601_duration = i['contentDetails']['duration']
            dt += isodate.parse_duration(iso_8601_duration)
        return dt

    def show_best_video(self):
        """Возвращает ссылку на видео с наибольшим колличеством лайков"""

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        url = ""
        count = 0
        for video in video_response['items']:
            count_video = int(video['statistics']['likeCount'])
            if count_video > count:
                count = int(video['statistics']['likeCount'])
                url = "https://youtu.be/" + video["id"]

        return url

