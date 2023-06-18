import json
import os
from googleapiclient.discovery import build


# from helper.youtube_api_manual import channel_id, youtube


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.id = self.channel["items"][0]["id"]
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.video_count = int(self.channel["items"][0]["statistics"]["videoCount"])
        self.subscriber_count = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.view_count = int(self.channel["items"][0]["statistics"]["viewCount"])
        self.url = "https://www.youtube.com/channel/" + self.id

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other: int) -> int:
        suma = self.subscriber_count + other.subscriber_count
        return suma

    def __sub__(self, other: int) -> int:
        suma = self.subscriber_count - other.subscriber_count
        return suma

    def __gt__(self, other: int) -> int:
        suma = self.subscriber_count > other.subscriber_count
        return suma

    def __ge__(self, other: int) -> int:
        suma = self.subscriber_count >= other.subscriber_count
        return suma

    def __lt__(self, other: int) -> int:
        suma = self.subscriber_count < other.subscriber_count
        return suma

    def __le__(self, other: int) -> int:
        suma = self.subscriber_count <= other.subscriber_count
        return suma


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.info_chanel = json.dumps(self.channel, indent=2, ensure_ascii=False)
        print(self.info_chanel)



    @classmethod
    def get_service(cls):
        """Возвращяем объет для работы с API youtube"""
        return cls.youtube

    @property
    def channel_id(self):
        """Возврощает объект с данными (snippet,statistics) youtube канала в формате json"""
        return self.channel

    @property
    def to_json(self):
        """Создаём файл json с данными youtube канала"""
        file_path = os.path.join(os.path.dirname(__file__), "moscowpython.json")
        with open(file_path, "a") as f:
            json.dump(self.channel, f, indent=2)
