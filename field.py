
import arcade
import random


class Field:

    def __init__(self):
        self.tile_size = 64

        # Загрузка текстур
        self.grass = arcade.load_texture("textures/grass.png")
        self.flowers_1 = arcade.load_texture("textures/grass_flowers_1.png")
        self.flowers_2 = arcade.load_texture("textures/grass_flowers_2.png")

        # Текстура вспаханной земли
        self.tilled_texture = arcade.load_texture(
            "textures/Поле без семян.png"
        )

        self.textures = [
            self.grass,
            self.flowers_1,
            self.flowers_2
        ]

        self.columns = 30
        self.rows = 12

        self.tile_sprites = arcade.SpriteList()

        # Генерация поля
        for row in range(self.rows):
            for column in range(self.columns):

                texture = random.choice(self.textures)

                sprite = arcade.Sprite(
                    texture,
                    scale=2,
                    center_x=column * self.tile_size + 32,
                    center_y=row * self.tile_size + 32
                )

                self.tile_sprites.append(sprite)

        # Таймер зарастания
        self.standing_tile = None
        self.standing_time = 0.0

    def till(self, x, y):

        column = int(x // self.tile_size)
        row = int(y // self.tile_size)

        if not (0 <= column < self.columns):
            return False

        if not (0 <= row < self.rows):
            return False

        index = row * self.columns + column
        sprite = self.tile_sprites[index]

        if sprite.texture == self.tilled_texture:
            return False

        sprite.texture = self.tilled_texture

        return True

    def update(self, delta_time, player_x, player_y,
               moving=False, interface_open=False):

        # При открытом интерфейсе время не считается
        if interface_open:
            return

        # Если игрок движется — сбрасываем таймер
        if moving:
            self.standing_tile = None
            self.standing_time = 0.0
            return

        # Определяем клетку под игроком
        column = int(player_x // self.tile_size)
        row = int(player_y // self.tile_size)

        if not (0 <= column < self.columns):
            self.standing_tile = None
            self.standing_time = 0.0
            return

        if not (0 <= row < self.rows):
            self.standing_tile = None
            self.standing_time = 0.0
            return

        index = row * self.columns + column
        sprite = self.tile_sprites[index]

        # Если земля не вспахана
        if sprite.texture != self.tilled_texture:
            self.standing_tile = None
            self.standing_time = 0.0
            return

        # Игрок перешёл на другую клетку
        if self.standing_tile != index:
            self.standing_tile = index
            self.standing_time = 0.0

        # Считаем время
        self.standing_time += delta_time

        # Через 5 секунд возвращаем обычную траву
        if self.standing_time >= 5.0:
            sprite.texture = self.grass

            self.standing_tile = None
            self.standing_time = 0.0

    def draw(self):
        self.tile_sprites.draw(pixelated=True)
