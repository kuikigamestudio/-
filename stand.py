
import arcade
import math


class Stand:

    def __init__(self):
        # Создание стойки
        self.stand = arcade.Sprite(
            "textures/stand.png",
            scale=0.1
        )

        self.stand.center_x = 160
        self.stand.center_y = 560

        # Создание мотыги
        self.hoe = arcade.Sprite(
            "textures/hoe.png",
            scale=2.5
        )

        # Положение мотыги внутри шкафа
        self.hoe.center_x = 160
        self.hoe.center_y = 560

        # Список стойки
        self.stand_list = arcade.SpriteList()
        self.stand_list.append(self.stand)

        # Список мотыги
        self.hoe_list = arcade.SpriteList()
        self.hoe_list.append(self.hoe)

        # Состояние мотыги
        self.hoe_available = True

        # Расстояние взаимодействия
        self.interaction_distance = 120

    def is_player_near(self, player):
        distance = math.hypot(
            player.center_x - self.stand.center_x,
            player.center_y - self.stand.center_y
        )

        return distance <= self.interaction_distance

    def update_hover(self, player, mouse_x, mouse_y):
        if not self.hoe_available:
            return

        if not self.is_player_near(player):
            self.hoe.color = (255, 255, 255)
            return

        if self.hoe.collides_with_point((mouse_x, mouse_y)):
            self.hoe.color = (85, 223, 255)
        else:
            self.hoe.color = (255, 255, 255)

    def take_hoe(self, player, mouse_x, mouse_y):
        if not self.hoe_available:
            return False

        if not self.is_player_near(player):
            return False

        if self.hoe.collides_with_point((mouse_x, mouse_y)):
            self.hoe_available = False
            return True

        return False

    def draw(self):
        # Сначала отрисовка стойки
        self.stand_list.draw(pixelated=True)

        # Затем отрисовка мотыги
        if self.hoe_available:
            self.hoe_list.draw(pixelated=True)
