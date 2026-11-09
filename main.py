
import arcade
import os

from field import Field
from player import Player
from cursor import Cursor
from gui import GameGUI
from economy import Economy


W, H = 1920, 720


def check_textures():
    textures = [
        "textures/grass.png",
        "textures/grass_flowers_1.png",
        "textures/grass_flowers_2.png",
        "textures/Игрок.png",
        "textures/stand.png",
        "textures/hoe.png",
        "textures/Поле без семян.png",
        "textures/curser aplle.png",
        "textures/money.png",
        "textures/shop.png"
    ]

    for texture in textures:
        if not os.path.exists(texture):
            print(f"Ошибка: не найдена текстура {texture}")


class MyLittleFarm(arcade.Window):

    def __init__(self):
        super().__init__(
            W,
            H,
            "My Little Farm",
            update_rate=1 / 60
        )

        arcade.set_background_color((100, 170, 100))

        check_textures()

        # ИГРОВОЙ МИР
        self.field = Field()

        self.player = Player()
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.cursor = Cursor(self.field)

        # ИНТЕРФЕЙС
        self.gui = GameGUI()

        # ЭКОНОМИКА
        self.economy = Economy()

        self.keys = set()
        self.mouse_held = False

        self.set_mouse_visible(False)

    def on_draw(self):
        self.clear()

        # Игровой мир
        self.field.draw()
        self.player_list.draw(pixelated=True)
        self.cursor.draw()

        # Экономика и магазин
        self.economy.draw(self.gui.active_tab)

        # Интерфейс поверх всего
        self.gui.draw()

    def on_update(self, delta_time):

        # ДВИЖЕНИЕ ИГРОКА
        self.player.change_x = 0
        self.player.change_y = 0

        if arcade.key.W in self.keys or arcade.key.UP in self.keys:
            self.player.change_y = 1

        if arcade.key.S in self.keys or arcade.key.DOWN in self.keys:
            self.player.change_y = -1

        if arcade.key.A in self.keys or arcade.key.LEFT in self.keys:
            self.player.change_x = -1

        if arcade.key.D in self.keys or arcade.key.RIGHT in self.keys:
            self.player.change_x = 1

        # Останавливаем персонажа только при открытом магазине
        if self.gui.active_tab is not None:
            self.player.change_x = 0
            self.player.change_y = 0
        else:
            self.player.update(delta_time)

        # АНИМАЦИЯ ИНТЕРФЕЙСА
        self.gui.update(delta_time)

        # ПРОВЕРКА ОТКРЫТЫХ ИНТЕРФЕЙСОВ
        interface_open = (
            self.gui.panel_open
            or self.gui.active_tab is not None
        )

        # ЗАРАСТАНИЕ ВСПАХАННОЙ ЗЕМЛИ
        self.field.update(
            delta_time,
            self.player.center_x,
            self.player.center_y,
            moving=(
                self.player.change_x != 0
                or self.player.change_y != 0
            ),
            interface_open=interface_open
        )

        # ВСПАШКА ПРИ УДЕРЖАНИИ ЛКМ
        if (
            self.mouse_held
            and self.gui.hoe_equipped
            and not self.gui.blocks_world_input(
                self.gui.mouse_x,
                self.gui.mouse_y
            )
        ):
            self.field.till(
                self.gui.mouse_x,
                self.gui.mouse_y
            )

    def on_key_press(self, symbol, modifiers):
        self.keys.add(symbol)

    def on_key_release(self, symbol, modifiers):
        self.keys.discard(symbol)

    def on_mouse_motion(self, x, y, dx, dy):
        self.gui.update_mouse(x, y)
        self.cursor.update_mouse(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.gui.update_mouse(x, y)
        self.cursor.update_mouse(x, y)

    def on_mouse_press(self, x, y, button, modifiers):

        self.gui.update_mouse(x, y)

        # Сначала проверяем интерфейс
        if self.gui.on_mouse_press(x, y):
            self.mouse_held = False
            return

        # Вспашка поля
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.gui.hoe_equipped:
                self.mouse_held = True

                if not self.gui.blocks_world_input(x, y):
                    self.field.till(x, y)

    def on_mouse_release(self, x, y, button, modifiers):

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_held = False


if __name__ == "__main__":
    game = MyLittleFarm()
    arcade.run()
