import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30
# Параметры
tile_size = 40 #Число кратное ширине и высоте экрана
num_rows = int(HEIGHT/tile_size)
num_columns = int(WIDTH/tile_size - 2)
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HALF_RED = (255, 0, 0, 128)


class Tile(pygame.sprite.Sprite):  # Клетка поля
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((38, 38))
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((38, 38))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 1
        self.rect.y = 1

    def update(self):
        if self.rect.left < 1:
            self.rect.left = 1
        if self.rect.right > WIDTH - 1:
            self.rect.right = WIDTH - 1
        if self.rect.top < 1:
            self.rect.top = 1
        if self.rect.bottom > HEIGHT - 1:
            self.rect.bottom = HEIGHT - 1

    def input(self, player_event):
        if player_event.type == pygame.KEYDOWN:
            if player_event.key == pygame.K_DOWN:
                self.rect.y += tile_size
            if player_event.key == pygame.K_UP:
                self.rect.y -= tile_size
            if player_event.key == pygame.K_RIGHT:
                self.rect.x += tile_size
            if player_event.key == pygame.K_LEFT:
                self.rect.x -= tile_size
            print(f"Tile Pos: {int(self.rect.x / tile_size), int(self.rect.y / tile_size)}")


# class FishingGame(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#
#         self.image = pygame.Surface((tile_size*2, HEIGHT))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect()
#         self.rect.x = WIDTH-tile_size*2


class FishingBar(pygame.sprite.Sprite):
    current_height = 0

    def __init__(self):  # Шкала прогресса по умолчанию(0 результат)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_size, 0 + self.current_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - tile_size
        self.rect.y = HEIGHT - self.current_height

        self.last_fishing_time = pygame.time.get_ticks()  # Время последнего пересечения
        self.space_reset_interval = 1000  # Интервал времени (в миллисекундах) для сброса счетчика

    def update(self):
        fishing = pygame.sprite.spritecollide(fishing_player, fish_rect, False)
        on_water = pygame.sprite.spritecollide(player, water_tiles, False)
        if on_water:
            if fishing:
                self.current_height += 2  # Увеличение шкалы
                self.__init__()
                self.last_space_press_time = pygame.time.get_ticks()
                if self.rect.y == 0:
                    print(f"Ура!")
                    self.current_height = 0
                    self.__init__()
            current_time = pygame.time.get_ticks()
            if current_time - self.last_space_press_time >= self.space_reset_interval:  # Уменьшение шкалы
                if self.current_height != 0:
                    self.current_height -= 2
                    self.__init__()

        else:  # Сброс шкалы
            self.current_height = 0
            self.__init__()

    # def update(self):
    #     collide = pygame.sprite.spritecollide(fish, fishing_player, False)
    #     if collide:


class FishingPlayer(pygame.sprite.Sprite):  # Удочка
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_size, 80), pygame.SRCALPHA) #Использование Алфа-канала
        self.image.fill(HALF_RED)
        self.rect = self.image.get_rect()

        self.fishing_player_speed = 5
        self.rect.x = WIDTH - tile_size * 2
        self.rect.y = HEIGHT
        self.space_pressed = False
        self.space_press_count = 0
        self.last_space_press_time = pygame.time.get_ticks()  # Время последнего нажатия "Пробел"
        self.space_reset_interval = 1000  # Интервал времени (в миллисекундах) для сброса счетчика

    def input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.space_pressed = True
                self.space_press_count += 1  # Увеличиваем счетчик нажатий "Пробел"
                # self.rect.y -= self.fishing_player_speed
                self.last_space_press_time = pygame.time.get_ticks()  # Записываем время нажатия "Пробел"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.space_pressed = False

    def update(self):
        collide = pygame.sprite.spritecollide(player, water_tiles, False)
        if collide:
            if self.space_pressed:  # Если клавиша "Пробел" нажата
                self.rect.y -= self.fishing_player_speed + self.space_press_count  # Вверх
            else:
                if self.rect.bottom < HEIGHT:  # Если не нажата клавиша "Пробел" и не достигнуто нижнее положение экрана
                    self.rect.y += self.fishing_player_speed + self.space_press_count  # Вниз

            current_time = pygame.time.get_ticks()
            if current_time - self.last_space_press_time >= self.space_reset_interval:
                self.space_press_count = 0  # Сбрасываем счетчик нажатий "Пробел"

            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
        else:
            self.rect.y = HEIGHT


class Fish(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_size, int(tile_size/2)))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.fish_speed = 5
        self.rect.x = WIDTH - tile_size * 2
        self.rect.y = HEIGHT
        self.direction = 1

    def update(self):
        collide = pygame.sprite.spritecollide(player, water_tiles, False)
        if collide:
            if self.rect.bottom > HEIGHT:
                self.direction = -1
            elif self.rect.top < 0:
                self.direction = 1
            self.rect.y += self.fish_speed * self.direction
        else:
            self.rect.y = HEIGHT


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GridFish")
clock = pygame.time.Clock()

# Группы
all_sprites = pygame.sprite.Group()
water_tiles = pygame.sprite.Group()
fish_rect = pygame.sprite.Group()

# Создание плиток травы
for row_index in range(num_rows):
    for col_index in range(num_columns):
        tile = Tile(GREEN)
        tile.rect.y = row_index * tile_size + 1
        tile.rect.x = col_index * tile_size + 1
        all_sprites.add(tile)

# Создание плиток воды
for i in range(10):
    tile = Tile(BLUE)
    tile.rect.x = random.randint(0, num_columns - 1) * tile_size + 1
    tile.rect.y = random.randint(0, num_rows - 1) * tile_size + 1
    all_sprites.add(tile)
    water_tiles.add(tile)

# Экземпляры
player = Player()
fish = Fish()
fishing_player = FishingPlayer()
fishing_bar = FishingBar()

fish_rect.add(fish)
all_sprites.add(player)
all_sprites.add(fish)
all_sprites.add(fishing_player)
all_sprites.add(fishing_bar)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.input(event)
        fishing_player.input(event)
    all_sprites.update()
    # Рендеринг
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
pygame.quit()
