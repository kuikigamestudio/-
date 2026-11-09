
import arcade


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("textures/Игрок.png", scale=2.5)

        self.center_x = 960
        self.center_y = 360

        self.speed = 250

        self.change_x = 0
        self.change_y = 0

        # Скорость поворота
        self.rotation_speed = 360

        # Целевой угол
        self.target_angle = 0

    def update(self, delta_time):
        # Передвижение
        self.center_x += self.change_x * self.speed * delta_time
        self.center_y += self.change_y * self.speed * delta_time

        # Определение направления
        if self.change_y > 0:
            self.target_angle = 0
        elif self.change_x > 0:
            self.target_angle = 90
        elif self.change_y < 0:
            self.target_angle = 180
        elif self.change_x < 0:
            self.target_angle = 270

        # Плавный поворот
        difference = (self.target_angle - self.angle + 180) % 360 - 180
        rotation_step = self.rotation_speed * delta_time

        if abs(difference) <= rotation_step:
            self.angle = self.target_angle
        else:
            self.angle += rotation_step if difference > 0 else -rotation_step

        # Границы поля
        self.left = max(self.left, 0)
        self.right = min(self.right, 1920)
        self.bottom = max(self.bottom, 0)
        self.top = min(self.top, 720)
