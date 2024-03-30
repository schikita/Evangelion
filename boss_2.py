import pygame
from fireball import Fireball  # Импортируем класс Fireball для использования в атаках босса

screen_width = 1000  # Устанавливаем ширину игрового экрана
screen_height = 800  # Устанавливаем высоту игрового экрана


class BossTwo(pygame.sprite.Sprite):  # Наследуемся от класса Sprite библиотеки Pygame
    def __init__(self, screen, image_sheet, position, all_sprites_group, fireballs_group):
        super().__init__()  # Вызываем конструктор родительского класса
        self.screen = screen  # Экран, на котором будет отображаться босс
        self.image_sheet = image_sheet  # Лист спрайтов босса
        self.rect = self.image_sheet.get_rect(topleft=position)  # Прямоугольник, определяющий положение и размеры босса на экране
        self.all_sprites = all_sprites_group  # Группа, содержащая все спрайты в игре
        self.fireballs = fireballs_group  # Группа для шаров огня, которые босс может выпустить
        self.health = 5  # Здоровье босса
        self.attack_frequency = 3000  # Частота атак босса (в миллисекундах)
        self.last_attack = pygame.time.get_ticks()  # Время последней атаки
        self.hit_time = 0  # Время, когда босс был последний раз поражен
        self.images = {  # Словарь с изображениями босса: обычное состояние и состояние после удара
            'normal': self.image_sheet.subsurface((0, 0, 184, 250)),  # Обычное изображение босса
            'hit': self.image_sheet.subsurface((184, 0, 184, 250))  # Изображение босса после попадания
        }
        self.image = self.images['normal']  # Текущее изображение босса

    def update(self):
        # Метод обновления состояния босса
        if pygame.time.get_ticks() - self.hit_time > 1000:  # Если с последнего попадания прошло более 1 секунды
            self.image = self.images['normal']  # Возвращаем обычное изображение
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > self.attack_frequency:  # Проверяем, пора ли атаковать
            self.fire()  # Выпускаем шар огня
            self.last_attack = current_time  # Обновляем время последней атаки

    def hit(self):
        # Метод, вызываемый при попадании в босса
        self.health -= 0.5  # Уменьшаем здоровье босса
        self.image = self.images['hit']  # Меняем изображение на "после попадания"
        self.hit_time = pygame.time.get_ticks()  # Запоминаем время попадания
        if self.health <= 0:
            self.kill()  # Если здоровье кончилось, удаляем босса из всех групп спрайтов
            self.show_level_complete()  # Показываем сообщение о завершении уровня

    def show_level_complete(self):
        # Метод отображения сообщения о завершении уровня
        font = pygame.font.Font(None, 74)  # Создаем шрифт
        text = font.render("Level complete", True, (255, 255, 255))  # Создаем текст
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))  # Центрируем текст
        self.screen.blit(text, text_rect)  # Рисуем текст на экране
        pygame.display.flip()  # Обновляем экран
        pygame.time.wait(5000)  # Задержка перед выходом в меню
        global current_screen, in_game  # Обновляем глобальные переменные для изменения состояния игры
        current_screen = "menu"
        in_game = False

    def fire(self):
        # Метод для атаки шаром огня
        fireball = Fireball(self.rect.midtop)  # Создаем объект Fireball
        self.fireballs.add(fireball)  # Добавляем его в группу fireballs
        self.all_sprites.add(fireball)  # Добавляем его в группу всех спрайтов
