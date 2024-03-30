import pygame
from fireball import Fireball  # Импортируем класс Fireball для создания огненных шаров, выпускаемых боссом

screen_width = 1000  # Устанавливаем ширину экрана
screen_height = 800  # Устанавливаем высоту экрана

class BossThree(pygame.sprite.Sprite):  # Класс третьего босса наследуется от Sprite для использования спрайтов Pygame
    def __init__(self, screen, image_sheet, position, all_sprites_group, fireballs_group):
        super().__init__()  # Вызываем инициализатор базового класса
        self.image_sheet = image_sheet  # Лист спрайтов, содержащий изображения босса
        self.screen = screen  # Экран, на котором будут отображаться спрайты
        # Словарь с изображениями босса: обычное и после получения урона
        self.images = {
            'normal': self.image_sheet.subsurface((0, 0, 240, 265)),  # Обычное состояние босса
            'hit': self.image_sheet.subsurface((260, 0, 230, 260))  # Состояние после попадания
        }
        self.image = self.images['normal']  # Устанавливаем изначальное изображение босса
        self.rect = self.image.get_rect(topleft=position)  # Получаем прямоугольник для позиционирования босса
        self.all_sprites = all_sprites_group  # Группа, содержащая все спрайты в игре
        self.fireballs = fireballs_group  # Группа для шаров огня, выпускаемых боссом
        self.health = 5  # Здоровье босса
        self.hit_time = 0  # Время последнего попадания
        self.attack_frequency = 3000  # Частота атак босса (в миллисекундах)
        self.last_attack = pygame.time.get_ticks()  # Время последней атаки для контроля частоты атак

    def update(self):
        # Метод обновления состояния босса
        if pygame.time.get_ticks() - self.hit_time > 1000:  # Если прошла 1 секунда после попадания
            self.image = self.images['normal']  # Возвращаем обычное изображение
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack > self.attack_frequency:  # Проверяем, пора ли атаковать
            self.fire()  # Босс выпускает огненный шар
            self.last_attack = current_time

    def hit(self):
        # Метод, вызываемый при попадании в босса
        self.health -= 0.5  # Уменьшаем здоровье босса
        self.image = self.images['hit']  # Меняем изображение на "после попадания"
        self.hit_time = pygame.time.get_ticks()  # Запоминаем время попадания
        if self.health <= 0:
            self.kill()  # Удаляем босса, если его здоровье на нуле
            self.show_level_complete()  # Показываем сообщение о завершении уровня

    def show_level_complete(self):
        # Отображение сообщения о завершении уровня
        font = pygame.font.Font(None, 74)  # Создаем шрифт
        text = font.render("Level complete", True, (255, 255, 255))  # Генерируем текст
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))  # Центрируем текст
        self.screen.blit(text, text_rect)  # Отображаем текст на экране
        pygame.display.flip()  # Обновляем содержимое экрана
        pygame.time.wait(5000)  # Задержка перед выходом в главное меню
        global current_screen, in_game
        current_screen = "menu"  # Возвращаемся в главное меню
        in_game = False

    def fire(self):
        # Выпускание огненного шара в сторону игрока
        fireball = Fireball(self.rect.midtop)  # Создаем экземпляр огненного шара
        self.fireballs.add(fireball)  # Добавляем его в группу огненных шаров
        self.all_sprites.add(fireball)  # Добавляем его в группу всех спрайтов
