
import arcade


class Cursor:

    def __init__(self, field):
        self.field = field
        self.tile_size = field.tile_size

        self.column = None
        self.row = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.color = (85, 223, 255)
        self.border_width = 1

        # Состояние мотыги
        self.hoe_equipped = False

        self.hoe = arcade.Sprite(
            "textures/hoe.png",
            scale=1.5
        )

        self.hoe_list = arcade.SpriteList()
        self.hoe_list.append(self.hoe)

    def pick_up_hoe(self):
        self.hoe_equipped = True

    def update_mouse(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

        column = int(x // self.tile_size)
        row = int(y // self.tile_size)

        if (0 <= column < self.field.columns and
                0 <= row < self.field.rows):
            self.column = column
            self.row = row
        else:
            self.column = None
            self.row = None

    def draw(self):
        # Рамка клетки
        if self.column is not None and self.row is not None:
            arcade.draw_lbwh_rectangle_outline(
                self.column * self.tile_size,
                self.row * self.tile_size,
                self.tile_size,
                self.tile_size,
                self.color,
                self.border_width
            )

        # Мотыга возле курсора
        if self.hoe_equipped:
            self.hoe.center_x = self.mouse_x + 20
            self.hoe.center_y = self.mouse_y - 20

            self.hoe_list.draw(pixelated=True)
