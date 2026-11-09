
import arcade


class Economy:

    def __init__(self):

        # Начальный баланс
        self.money = 10

        # Монетка
        self.coin = arcade.Sprite(
            "textures/money.png"
        )

        self.coin.center_x = 42
        self.coin.center_y = 38
        self.coin.width = 32
        self.coin.height = 32

        self.coin_list = arcade.SpriteList()
        self.coin_list.append(self.coin)

    def add_money(self, amount):
        self.money += amount

    def spend_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True

        return False

    def draw(self, active_tab=None):

        # Денежная подложка
        arcade.draw_lbwh_rectangle_filled(
            10, 8,
            135, 60,
            (15, 15, 20, 210)
        )

        arcade.draw_lbwh_rectangle_outline(
            10, 8,
            135, 60,
            (100, 110, 100, 220),
            2
        )

        # Монетка
        self.coin_list.draw(pixelated=True)

        # Баланс
        arcade.draw_text(
            str(self.money),
            73, 24,
            (0, 0, 0),
            27,
            bold=True
        )

        arcade.draw_text(
            str(self.money),
            71, 26,
            (50, 255, 90),
            27,
            bold=True
        )

        # СОДЕРЖИМОЕ ВКЛАДКИ МАГАЗИНА
        if active_tab == "shop":

            window_width = 700
            window_height = 400

            x = 610
            y = 160

            arcade.draw_lbwh_rectangle_filled(
                x,
                y,
                window_width,
                window_height,
                (20, 25, 30, 245)
            )

            arcade.draw_lbwh_rectangle_outline(
                x,
                y,
                window_width,
                window_height,
                (180, 200, 160, 255),
                3
            )

            arcade.draw_text(
                "Окно высветилось",
                x + 170,
                y + 190,
                (255, 255, 255),
                30,
                bold=True
            )
