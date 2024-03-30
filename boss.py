import pygame
from fireball import Fireball  # Импорт класса Fireball для использования в атаках босса

screen_width = 1000  # Ширина игрового окна
screen_height = 800  # Высота игрового окна


class Boss(pygame.sprite.Sprite):  # Класс Boss наследуется от Sprite в Pygame для удобной работы со спрайтами
    def __init__(self, screen, image_sheet, position, all_sprites_group, fireballs_group):
        super().__init__()  # Инициализация базового класса
        self.image_sheet = image_sheet  # Лист со спрайтами босса
        self.screen = screen  # Сохраняем screen как атрибут класса
        self.images = {     # Словарь для хранения изображений босса: обычное и после получения урона
            'normal': self.image_sheet.subsurface((0, 0, 240, 240)),
            'hit': self.image_sheet.subsurface((250, 0, 240, 240))  # Исправлено на корректные размеры
        }
        self.image = self.images['normal']      # Текущее изображение босса
        self.rect = self.image.get_rect(topleft=position)       # Прямоугольник для позиционирования и коллизий
        self.all_sprites = all_sprites_group        # Группа всех спрайтов для взаимодействия с игровым миром
        self.fireballs = fireballs_group        # Группа шаров огня, которые может выпускать босс
        self.health = 5  # Пять жизней у босса
        self.hit_time = 0
        self.attack_frequency = 3000  # Частота атаки в миллисекундах
        self.last_attack = pygame.time.get_ticks()  # Время последней атаки

    def update(self):       # Метод обновления состояния босса
        # Проверка состояния "попадание"
        if pygame.time.get_ticks() - self.hit_time > 1000:  # Если прошла 1 секунда после попадания
            self.image = self.images['normal']
        # Дополнительная логика обновления (например, стрельба)
        # Дополнительная логика обновления
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > self.attack_frequency:     # Если пора атаковать
            self.fire()     # Выпускаем шар огня
            self.last_attack = current_time

    def hit(self):  # Вызывается при попадании копья игрока
        self.health -= 0.5      # Уменьшаем здоровье
        self.image = self.images['hit']
        self.hit_time = pygame.time.get_ticks()  # Запоминаем время попадания
        if self.health <= 0:        # Если здоровье закончилось
            self.kill()  # Удаление босса при смерти
            self.show_level_complete()  # Показываем сообщение о завершении уровня

    def show_level_complete(self):      # Метод отображения сообщения о завершении уровня
        font = pygame.font.Font(None, 74)       # Создаем шрифт
        text = font.render("Level complete", True, (255, 255, 255))     # Создаем текст
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))     # Центрируем текст
        self.screen.blit(text, text_rect)       # Рисуем текст на экране
        pygame.display.flip()       # Обновляем экран
        pygame.time.wait(5000)      # Пауза на 5 секунд
        global current_screen, in_game      # Обновляем глобальные переменные для выхода в меню
        current_screen = "menu"
        in_game = False

    def fire(self):     # Метод для атаки шарами огня
        # Запуск шарика в сторону игрока
        fireball = Fireball(self.rect.midtop)       # Создаем шар огня на верхушке босса
        self.fireballs.add(fireball)        # Добавляем шар огня в группу
        self.all_sprites.add(fireball)      # Добавляем шар огня в группу всех спрайтов для отображения и взаимодействия
