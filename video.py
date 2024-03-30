import pygame
import os  # Для работы с файловой системой
from ffpyplayer.player import MediaPlayer  # Библиотека для воспроизведения медиа
from ffpyplayer.tools import set_loglevel  # Для управления уровнем логирования ffpyplayer
from pymediainfo import MediaInfo  # Для получения информации о медиафайлах
from errno import ENOENT  # Код ошибки "No such file or directory"


class Video:
    def __init__(self, path):  # Используем двойные подчеркивания для определения конструктора
        if not os.path.exists(path):  # Проверка на существование файла по указанному пути
            raise FileNotFoundError(ENOENT, os.strerror(ENOENT), path)  # Вызов исключения, если файла нет
        set_loglevel("quiet")  # Установка тихого режима логирования для ffpyplayer

        self.path = path  # Путь к видеофайлу
        self.name = os.path.splitext(os.path.basename(path))[0]     # Имя файла без расширения

        self._video = MediaPlayer(path)     # Создание объекта MediaPlayer для воспроизведения видео
        self.set_volume(0)  # Устанавливаем громкость на 0
        self._frame_num = 0

        info = MediaInfo.parse(path).video_tracks[0]    # Получение информации о видеодорожке

        # Инициализация свойств видео на основе полученной информации
        self.frame_rate = float(info.frame_rate)
        self.frame_count = int(info.frame_count)
        self.frame_delay = 1 / self.frame_rate      # Задержка между кадрами в секундах
        self.duration = info.duration / 1000        # Длительность видео в секундах
        self.original_size = (info.width, info.height)  # Исходное разрешение видео
        self.current_size = self.original_size  # Текущее разрешение видео

        self.active = True  # Флаг активности видео (воспроизводится или нет)
        self.frame_surf = pygame.Surface((1, 1))    # Поверхность для отрисовки текущего кадра видео

        self.alt_resize = pygame.transform.smoothscale  # Метод для изменения размера изображения

    def close(self):
        # Метод закрытия видеоплеера и деактивации видео
        self._video.close_player()
        self.active = False  # Деактивируем видео после закрытия

    def restart(self):
        # Метод перезапуска видео
        self._video = MediaPlayer(self.path)  # Пересоздаем объект MediaPlayer
        self._frame_num = 0
        self.frame_surf = None  # Сбрасываем surface кадра
        self.active = True  # Снова активируем видео

    def set_size(self, size: tuple):
        # Установка нового размера видео
        self._video.set_size(*size)
        self.current_size = size

    # volume goes from 0.0 to 1.0
    def set_volume(self, volume: float):
        # Установка громкости воспроизведения
        self._video.set_volume(volume)

    def get_volume(self) -> float:
        # Получение текущей громкости воспроизведения
        return self._video.get_volume()

    def get_paused(self) -> bool:
        # Получение статуса паузы видео
        return self._video.get_pause()

    def pause(self):
        # Пауза воспроизведения
        self._video.set_pause(True)

    def resume(self):
        # Возобновление воспроизведения
        self._video.set_pause(False)

    # gets time in seconds
    def get_pos(self) -> float:

        return self._video.get_pts()

    def toggle_pause(self):
        # Переключение статуса паузы
        self._video.toggle_pause()

    def _update(self):
        # Внутренний метод обновления видео (проверка кадров и их обновление)
        # Возвращает True, если кадр был обновлен
        updated = False

        if self._frame_num + 1 == self.frame_count:
            self.active = False
            return False

        while self._video.get_pts() > self._frame_num * self.frame_delay:
            frame = self._video.get_frame()[0]
            self._frame_num += 1

            if frame != None:
                size = frame[0].get_size()
                img = pygame.image.frombuffer(frame[0].to_bytearray()[0], size, "RGB")
                if size != self.current_size:
                    img = self.alt_resize(img, self.current_size)
                self.frame_surf = img

                updated = True

        return updated

    # seek uses seconds
    def seek(self, seek_time: int):
        # Перемотка видео на указанное количество секунд
        vid_time = self._video.get_pts()
        if vid_time + seek_time < self.duration and self.active:
            self._video.seek(seek_time)
            while vid_time + seek_time < self._frame_num * self.frame_delay:
                self._frame_num -= 1

    def draw(self, surf: pygame.Surface, pos: tuple, force_draw: bool = True) -> bool:
        # Отрисовка текущего кадра видео на переданной поверхности
        if self.active and (self._update() or force_draw):
            if self.frame_surf is not None:  # Добавляем эту проверку
                surf.blit(self.frame_surf, pos)
                return True
        return False
