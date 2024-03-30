import pygame
from spear import Spear  # Импорт класса Spear для создания объектов копий

screen_height = 800  # Высота игрового экрана


class Player(pygame.sprite.Sprite):  # Наследуется от класса Sprite в Pygame
    def __init__(self, image_sheet, position, all_sprites_group, spears_group, screen_height):
        super().__init__()  # Инициализация базового класса
        self.screen_height = screen_height  # Высота экрана, используется для проверки приземления
        self.image_sheet = image_sheet  # Лист спрайтов игрока
        self.all_sprites = all_sprites_group  # Группа всех спрайтов в игре
        self.spears = spears_group  # Группа спрайтов копий
        self.last_direction = "right"  # Последнее направление движения игрока
        self.state = "standing"  # Текущее состояние игрока (стоит, бежит, приседает и т.д.)
        self.anim_index = 0  # Индекс текущего кадра анимации
        self.anim_timer = pygame.time.get_ticks()  # Таймер для обновления анимации
        self.velocity = 1  # Скорость перемещения игрока по горизонтали
        self.jump_speed = -14  # Начальная скорость прыжка
        self.gravity = 0.2  # Гравитация, влияющая на прыжок и падение
        self.on_ground = True  # Находится ли игрок на земле
        self.y_velocity = 0  # Вертикальная скорость игрока
        # Определение прямоугольников для каждого состояния игрока в листе спрайтов
        self.frame_rects = {
            # Каждое состояние имеет список прямоугольников, соответствующих кадрам анимации
        }
        self.update_rect(position)  # Обновление позиции и изображения игрока
        self.health = 5  # Количество жизней игрока

    def update_rect(self, position):
        # Обновление позиции и изображения игрока в соответствии с текущим состоянием и кадром анимации
        # Извлечение соответствующего кадра из листа спрайтов и установка его как текущего изображения
        # Установка позиции игрока
        frame_rects = {
            "standing": (0, 0, 150, 150),
            "running_forward": [(150, 0, 150, 150), (300, 0, 150, 150)],
            "running_backward": [(150, 150, 150, 150), (300, 150, 150, 150)],
            "backward_standing": (0, 150, 150, 150),
            "jumping_forward": (0, 300, 150, 150),
            "jumping_backward": (0, 450, 150, 150),
            "crouching_forward": (0, 340, 150, 110),
            "crouching_backward": (0, 300, 150, 150),
            "attacking_forward": (150, 300, 150, 150),
            "attacking_backward": (150, 450, 150, 150),
        }
        frame = frame_rects[self.state][self.anim_index] if isinstance(frame_rects[self.state], list) else frame_rects[
            self.state]
        self.image = self.image_sheet.subsurface(frame)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self, keys):
        # Обновление состояния игрока: обработка нажатий клавиш и применение гравитации
        current_time = pygame.time.get_ticks()
        if self.on_ground:
            if keys[pygame.K_LEFT]:
                self.move(-self.velocity, "running_backward")
            elif keys[pygame.K_RIGHT]:
                self.move(self.velocity, "running_forward")
            elif keys[pygame.K_DOWN]:
                self.crouch()
            elif keys[pygame.K_SPACE]:
                self.throw_spear()
            elif keys[pygame.K_UP]:
                self.jump()
            else:
                self.stand()

        self.apply_gravity()

    def move(self, velocity, state):
        # Движение игрока: обновление позиции и состояния
        self.rect.x += velocity
        self.state = state
        self.last_direction = "right" if velocity > 0 else "left"
        self.update_animation()

    def crouch(self):
        self.state = "crouching_forward" if self.last_direction == "right" else "crouching_backward"
        self.update_animation()

    def stand(self):
        # Приседание: обновление состояния игрока
        self.state = "standing"
        self.update_animation()

    def jump(self):
        # Прыжок: обновление вертикальной скорости и состояния игрока
        if self.on_ground:
            self.y_velocity = self.jump_speed
            self.on_ground = False
            self.state = "jumping_forward" if self.last_direction == "right" else "jumping_backward"
            self.anim_index = 0  # Сброс анимации
            self.update_animation()

    def apply_gravity(self):
        # Применение гравитации: обновление вертикальной скорости и проверка приземления
        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity
        if self.rect.bottom > 750:
            self.rect.bottom = 750
            self.on_ground = True
            self.y_velocity = 0

        # Плавное замедление перед приземлением
        if self.rect.bottom >= screen_height - 100 and self.y_velocity > 0:  # Если персонаж находится на высоте 100px от земли и движется вниз
            self.y_velocity *= 0.8  # Замедляем скорость падения

        # Проверка приземления на землю
        if self.rect.bottom > screen_height - 50:
            self.rect.bottom = screen_height - 50
            self.on_ground = True
            self.y_velocity = 0

    def throw_spear(self):
        # Бросок копья: создание нового объекта копья и его добавление в соответствующие группы спрайтов
        if not self.state.startswith('attacking'):
            spear = Spear((self.rect.centerx + (50 if self.last_direction == "right" else -50), self.rect.centery))
            self.all_sprites.add(spear)
            self.spears.add(spear)
            self.state = "attacking_forward" if self.last_direction == "right" else "attacking_backward"
            self.update_animation()

    def update_animation(self):
        # Обновление анимации: изменение кадра анимации в зависимости от времени
        current_time = pygame.time.get_ticks()
        if current_time - self.anim_timer > 100:
            self.anim_index = (self.anim_index + 1) % len(self.frame_rects[self.state])
            self.anim_timer = current_time
            self.update_rect(self.rect.topleft)

    def take_damage(self):
        # Получение урона: уменьшение количества жизней и обновление изображения игрока
        self.health -= 1
        # Загрузка и установка спрайта игрока, соответствующего получению урона
        damage_frame = self.image_sheet.subsurface((0, 600, 150, 150))  # Выбираем часть спрайта
        self.image = damage_frame
        if self.health <= 0:
            self.die()
        else:
            # Возвращаем оригинальный спрайт через 0.5 секунды
            pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # Используем пользовательское событие для задержки

    def die(self):
        # Обработка смерти игрока
        global current_screen
        current_screen = "menu"
        # Отображение сообщения "You lose" можно сделать здесь или в главном цикле
