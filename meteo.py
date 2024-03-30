import pygame
import random  # Импортируем модуль random для генерации случайных чисел

class Meteo(pygame.sprite.Sprite):  # Класс метеорита, наследующийся от Sprite
    def __init__(self, image, screen_width, screen_height):
        super().__init__()  # Вызов конструктора базового класса
        self.image = image  # Устанавливаем изображение метеорита, переданное при создании экземпляра
        self.rect = self.image.get_rect()  # Получаем прямоугольник вокруг метеорита для определения его положения и коллизий
        # Устанавливаем начальную позицию метеорита случайным образом в пределах ширины экрана и выше верхнего края экрана
        self.rect.x = random.randint(0, screen_width - self.rect.width)  # Случайная начальная позиция по оси X
        self.rect.y = random.randint(-100, -10)  # Случайная начальная позиция по оси Y (выше экрана)
        self.speed = 0.58  # Устанавливаем скорость метеорита
        self.screen_height = screen_height  # Сохраняем высоту экрана для дальнейшего использования

    def update(self):
        self.rect.y += self.speed  # Перемещаем метеорит вниз с заданной скоростью
        if self.rect.top > self.screen_height:  # Если метеорит полностью покидает экран снизу
            self.kill()  # Удаляем метеорит из всех групп спрайтов и из игры
