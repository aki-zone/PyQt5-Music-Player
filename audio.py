import base64
import json
import os
import sys
import threading
from typing import List
from pydub import AudioSegment
import eyed3
import pygame
from pydub.utils import mediainfo


class PlayBean:
    """
    音乐播放器，根据地址、音量、时间戳播放音乐文件
    """
    def __init__(self, start_time=0, volume=0):
        self.start_time = start_time  # 用于跟踪当前播放的时间
        self.playing = False  # 用于跟踪音乐播放状态
        self.volume = volume

    def play_music(self, start_time, volume, file_path):

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)

        self.playing = True  # 设置播放状态为True
        self.start_time = start_time
        self.volume = volume
        self.music_length = pygame.mixer.Sound(file_path).get_length()


        def play_thread():
            """
            这里需要多线程操作以供播放器在播放音乐的同时可以进行其他任务
            """

            # 设置音量
            pygame.mixer.music.set_volume(self.volume / 100)

            # 开始播放
            pygame.mixer.music.play()

            # 设置开始播放的时间
            if self.start_time > self.music_length:
                self.start_time = 0
            pygame.mixer.music.set_pos(self.start_time)

            # 循环检测音乐是否播放结束
            clock = pygame.time.Clock()

            pin = 0
            while pygame.mixer.music.get_busy() and self.start_time < self.music_length:
                self.start_time += (pygame.mixer.music.get_pos() / 1000 - pin)
                # 设置音量
                pygame.mixer.music.set_volume(self.volume / 100)
                self.playing = True
                pin = pygame.mixer.music.get_pos() / 1000
                clock.tick(900)  # 控制循环速度，避免过度占用CPU

            # 播放结束，更新 playing
            self.playing = False  # 播放结束，将播放状态设为False

        # 创建线程并启动
        playThread = threading.Thread(target=play_thread)
        playThread.start()

    def pause_music(self): # 暂停
        pygame.mixer.music.pause()
        self.playing = False  # 暂停后将播放状态设为False

    def stop_music(self): # 停止
        pygame.mixer.music.stop()
        self.start_time = 0
        self.playing = False  # 停止后将播放状态设为False

    def is_busy(self): # 判断音乐器是否在播放中
        return self.playing

    def get_len(self):  # 返回音乐长度
        return self.music_length

    def set_start(self, value): # 设置全局音乐起始播放时间戳
        self.start_time = value

    def set_volume(self, value): # 设置全局音乐起始播放音量值
        self.volume = value


class MusicReader:

    """
    获取音乐文件信息，包括但不限于：标题，艺术家，专辑名，大小，时长，地址，封面二进制流，MIME
    """
    def __init__(self, file_path):
        self.audiofile = ""
        self.album_MIME = ""
        self.album_cover = None
        self.filename = ""
        self.size_bytes = 0
        self.album = ""
        self.artist = ""
        self.title = ""
        self.music_length = 100
        self.file_path = file_path

        # 根据文件后缀选择解析库
        file_extension = os.path.splitext(self.file_path)[1].lower()

        # TODO 暂时仅完成了mp3格式的解析
        if file_extension == '.mp3':
            self.load_mp3_info()

        # elif file_extension == '.flac':
        #    self.load_flac_info()

    def to_dict(self):
        return {
            'file_path': self.file_path,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'size_bytes': self.size_bytes,
            'filename': self.filename,
            'album_cover': base64.b64encode(self.album_cover).decode('utf-8') if self.album_cover else None,
            'album_MIME': self.album_MIME,
            'music_length': self.music_length
        }

    def import_music_info_from_json(self, json_data: str):
        """
        json导入函数
        """
        data = json.loads(json_data)
        self.title = data.get('title', "")
        self.artist = data.get('artist', "")
        self.album = data.get('album', "")
        self.size_bytes = data.get('size_bytes', None)
        self.filename = data.get('filename', "")

        album_cover_str = data.get('album_cover')
        self.album_cover = base64.b64decode(album_cover_str) if album_cover_str else None

        self.album_MIME = data.get('album_MIME', "")
        self.music_length = data.get('music_length', None)

    # ------------------调试类函数------------------------

    def display_metadata(self):
        """
        全信息输出函数
        """
        print(f"标题: {self.title}")
        print(f"艺术家: {self.artist}")
        print(f"专辑: {self.album}")
        print(f"大小 (bytes): {self.size_bytes}")
        print(f"文件名: {self.filename}")
        print(f"MIME: {self.album_MIME}")
        print(f"音乐总时长 (毫秒): {self.music_length}")
        if self.album_cover:
            print("专辑封面: 存在")
            print(self.album_cover)
        else:
            print("专辑封面: 空白")

    def get_info_str(self) -> str:
        """
        全信息转为str格式函数
        """
        metadata_str = f"标题: {self.title}\n"
        metadata_str += f"艺术家: {self.artist}\n"
        metadata_str += f"专辑: {self.album}\n"
        metadata_str += f"大小: {self.size_bytes / (1024 * 1024):.2f}  (MB)\n"
        metadata_str += f"文件名: {self.filename}\n"
        metadata_str += f"MIME: {self.album_MIME}\n"
        metadata_str += f"音乐总时长: {self.music_length / 1000}  (秒)\n"
        return metadata_str

    def load_mp3_info(self):
        """
        获取mp3文件信息函数，这里使用eyed3作为解析库
        """
        self.audiofile = eyed3.load(self.file_path)
        if self.audiofile.tag:
            # 读取元信息
            self.title = self.audiofile.tag.title
            self.artist = self.audiofile.tag.artist
            self.album = self.audiofile.tag.album
            self.size_bytes = self.audiofile.info.size_bytes
            self.filename = self.audiofile.path

            # 读取专辑封面
            if self.audiofile.tag.images:
                self.album_cover = self.audiofile.tag.images[0].image_data
                self.album_MIME = self.audiofile.tag.images[0].mime_type
        else:
            self.title = None
            self.artist = None
            self.album = None
            self.size_bytes = None
            self.filename = None
            self.album_cover = None
            self.album_MIME = None

        # 获取音乐时长（单位：毫秒）
        self.music_length = int(self.audiofile.info.time_secs * 1000) if self.audiofile.info else None

    # TODO 关于flac格式解析算法暂时无法完成
    def load_flac_info(self):
        pass


class Config:
    """
    单元配置函数，储存当前音乐文件信息，以及其被预设好、操作过的各种播放信息
    例如：播放时间点，播放音量，归属目录地址...
    """
    def __init__(self, music_list: List[str] = None, volume: int = 50, music_url: str = "",
                 music_now: float = 0.0, music_info: MusicReader = None, music_dir: str = ""):
        self.music_list = music_list
        self.music_url = music_url
        self.volume = volume
        self.music_now = music_now
        self.music_dir = music_dir

        if music_info is None and music_url is not None:
            self.music_info = MusicReader(music_url)
        else:
            self.music_info = music_info

    def set_volume(self, volume: int):
        self.volume = volume

    def set_music_url(self, music_url: str):
        self.music_url = music_url

    def set_music_now(self, music_now: float):
        self.music_now = music_now

    def set_music_info(self, music_info: MusicReader):
        self.music_info = music_info

    def set_music_dir(self, music_dir: str):
        self.music_dir = music_dir

    def import_config_from_json(self, json_data: str):
        """
        json导入函数
        """
        data = json.loads(json_data)

        self.music_list = data.get('music_list', [])
        self.volume = data.get('volume', 50)
        self.music_url = data.get('music_url', None)
        self.music_dir = data.get('music_dir', None)
        self.music_now = data.get('music_now', 0.0)

        music_info_data = data.get('music_info', {})
        music_reader = MusicReader('')
        music_reader.import_music_info_from_json(json.dumps(music_info_data))

        self.music_info = music_reader

    def save_config_file(self, filename="config.json"):
        """
        保存json文件，以供下次启动程序时初始化。这里可以用全局变量，暂时没做修改
        """
        config_data = self.export_config_to_json()
        with open(filename, 'w') as file:
            file.write(config_data)

    def export_config_to_json(self) -> str:
        """
        导出信息数据为json格式字典
        """
        data = {
            'music_list': self.music_list,
            'volume': self.volume,
            'music_url': self.music_url,
            'music_now': self.music_now,
            'music_dir': self.music_dir,
            'music_info': self.music_info.to_dict() if self.music_info else None
        }
        return json.dumps(data)

    def load_config_file(self, filename="config.json"):
        """
        加载json格式文件，读入到程序里
        """
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                config_data = file.read()
                self.import_config_from_json(config_data)

    # ----------------调试代码--------------------
    def display_all_info(self):
        print("音乐列表:", self.music_list)
        print("音量:", self.volume)
        print("当前音乐地址:", self.music_url)
        print("当前音乐时间截点:", self.music_now)
        print("当前播放目录:", self.music_dir)
        if self.music_info:
            pass
            # self.music_info.display_metadata()
