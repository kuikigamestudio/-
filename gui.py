
import arcade


class GameGUI:

    def __init__(self):
        self.panel_open = False
        self.panel_progress = 0.0

        self.selected_tool = "cursor"
        self.active_tab = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.window_width = 1920
        self.window_height = 720

        # Правая панель
        self.sidebar_width = 100
        self.sidebar_x = self.window_width - self.sidebar_width

        # Текстуры
        self.cursor_texture = arcade.load_texture(
            "textures/curser aplle.png"
        )

        self.hoe_texture = arcade.load_texture(
            "textures/hoe.png"
        )

        self.shop_texture = arcade.load_texture(
            "textures/shop.png"
        )

        # ШКАФ
        self.cabinet = arcade.Sprite("textures/stand.png")
        self.cabinet.center_x = 1870
        self.cabinet.center_y = 610
        self.cabinet.width = 64
        self.cabinet.height = 64

        self.cabinet_list = arcade.SpriteList()
        self.cabinet_list.append(self.cabinet)

        self.cabinet_hover = 0.0

        # КНОПКА SHOP
        self.shop_icon = arcade.Sprite(self.shop_texture)
        self.shop_icon.center_x = 1870
        self.shop_icon.center_y = 520
        self.shop_icon.width = 64
        self.shop_icon.height = 64

        self.shop_list = arcade.SpriteList()
        self.shop_list.append(self.shop_icon)

        self.shop_hover = 0.0

        # ИКОНКИ ИНСТРУМЕНТОВ
        self.cursor_icon = arcade.Sprite(self.cursor_texture)
        self.hoe_icon = arcade.Sprite(self.hoe_texture)

        self.cursor_icon_list = arcade.SpriteList()
        self.hoe_icon_list = arcade.SpriteList()

        self.cursor_icon_list.append(self.cursor_icon)
        self.hoe_icon_list.append(self.hoe_icon)

        self.cursor_hover = 0.0
        self.hoe_hover = 0.0

        # СОБСТВЕННЫЙ КУРСОР
        self.pointer = arcade.Sprite(
            self.cursor_texture,
            scale=1.0
        )

        self.pointer_list = arcade.SpriteList()
        self.pointer_list.append(self.pointer)

        # ПАНЕЛЬ ИНСТРУМЕНТОВ
        self.panel_x = 1450
        self.panel_y = 300
        self.panel_width = 400
        self.panel_height = 220

        self.cursor_button = (1550, 405)
        self.hoe_button = (1720, 405)

    @property
    def hoe_equipped(self):
        return self.selected_tool == "hoe"

    def smooth(self, current, target, delta_time, speed=12):
        amount = min(1.0, delta_time * speed)
        return current + (target - current) * amount

    def update_mouse(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def update(self, delta_time):

        # Анимация панели инструментов
        target = 1.0 if self.panel_open else 0.0

        self.panel_progress = self.smooth(
            self.panel_progress,
            target,
            delta_time,
            10
        )

        # Наведение на шкаф
        hovering = self.cabinet.collides_with_point(
            (self.mouse_x, self.mouse_y)
        )

        self.cabinet_hover = self.smooth(
            self.cabinet_hover,
            1.0 if hovering else 0.0,
            delta_time
        )

        cabinet_size = 64 + 7 * self.cabinet_hover
        self.cabinet.width = cabinet_size
        self.cabinet.height = cabinet_size

        # Наведение на SHOP
        hovering = self.shop_icon.collides_with_point(
            (self.mouse_x, self.mouse_y)
        )

        self.shop_hover = self.smooth(
            self.shop_hover,
            1.0 if hovering else 0.0,
            delta_time
        )

        shop_size = 64 + 7 * self.shop_hover
        self.shop_icon.width = shop_size
        self.shop_icon.height = shop_size

        # Анимация инструментов
        offset = (1 - self.panel_progress) * 430

        cursor_x = self.cursor_button[0] + offset
        hoe_x = self.hoe_button[0] + offset

        cursor_y = self.cursor_button[1]
        hoe_y = self.hoe_button[1]

        cursor_is_hovered = (
            self.panel_progress > 0.1
            and abs(self.mouse_x - cursor_x) < 45
            and abs(self.mouse_y - cursor_y) < 45
        )

        hoe_is_hovered = (
            self.panel_progress > 0.1
            and abs(self.mouse_x - hoe_x) < 45
            and abs(self.mouse_y - hoe_y) < 45
        )

        self.cursor_hover = self.smooth(
            self.cursor_hover,
            1.0 if cursor_is_hovered else 0.0,
            delta_time
        )

        self.hoe_hover = self.smooth(
            self.hoe_hover,
            1.0 if hoe_is_hovered else 0.0,
            delta_time
        )

        # Позиции и размеры иконок
        self.cursor_icon.center_x = cursor_x
        self.cursor_icon.center_y = cursor_y

        self.hoe_icon.center_x = hoe_x
        self.hoe_icon.center_y = hoe_y

        self.cursor_icon.width = 58 + 9 * self.cursor_hover
        self.cursor_icon.height = 58 + 9 * self.cursor_hover

        self.hoe_icon.width = 58 + 9 * self.hoe_hover
        self.hoe_icon.height = 58 + 9 * self.hoe_hover

        # Курсор мыши
        self.pointer.center_x = self.mouse_x
        self.pointer.center_y = self.mouse_y

        if self.hoe_equipped:
            self.pointer.texture = self.hoe_texture
        else:
            self.pointer.texture = self.cursor_texture

    def blocks_world_input(self, x, y):

        if x >= self.sidebar_x:
            return True

        if self.panel_progress > 0.01:

            offset = (1 - self.panel_progress) * 430

            left = self.panel_x + offset
            right = left + self.panel_width

            if left <= x <= right and 280 <= y <= 550:
                return True

        return False

    def on_mouse_press(self, x, y):

        # Открытие инструментов через шкаф
        if self.cabinet.collides_with_point((x, y)):
            self.panel_open = not self.panel_open
            self.active_tab = None
            return True

        # Открытие и закрытие магазина
        if self.shop_icon.collides_with_point((x, y)):
            self.panel_open = False

            if self.active_tab == "shop":
                self.active_tab = None
            else:
                self.active_tab = "shop"

            return True

        # Выбор курсора или мотыги
        if self.panel_progress > 0.9:

            offset = (1 - self.panel_progress) * 430

            cursor_x = self.cursor_button[0] + offset
            hoe_x = self.hoe_button[0] + offset

            if (
                abs(x - cursor_x) < 45
                and abs(y - self.cursor_button[1]) < 45
            ):
                self.selected_tool = "cursor"
                self.panel_open = False
                return True

            if (
                abs(x - hoe_x) < 45
                and abs(y - self.hoe_button[1]) < 45
            ):
                self.selected_tool = "hoe"
                self.panel_open = False
                return True

        return self.blocks_world_input(x, y)

    def draw(self):

        # Правая панель
        arcade.draw_lbwh_rectangle_filled(
            self.sidebar_x,
            0,
            self.sidebar_width,
            self.window_height,
            (15, 15, 20, 190)
        )

        arcade.draw_line(
            self.sidebar_x,
            0,
            self.sidebar_x,
            self.window_height,
            (100, 100, 115, 180),
            2
        )

        # Шкаф и SHOP
        self.cabinet_list.draw(pixelated=True)
        self.shop_list.draw(pixelated=True)

        # Меню инструментов
        if self.panel_progress > 0.01:

            offset = (1 - self.panel_progress) * 430

            x = self.panel_x + offset
            y = self.panel_y

            alpha = int(105 * self.panel_progress)
            text_alpha = int(255 * self.panel_progress)

            arcade.draw_lbwh_rectangle_filled(
                x,
                y,
                self.panel_width,
                self.panel_height,
                (20, 25, 30, alpha)
            )

            arcade.draw_lbwh_rectangle_outline(
                x,
                y,
                self.panel_width,
                self.panel_height,
                (180, 200, 160, text_alpha),
                3
            )

            arcade.draw_text(
                "Инструменты",
                x + 25,
                y + 175,
                (255, 255, 255, text_alpha),
                22
            )

            self.cursor_icon_list.draw(pixelated=True)
            self.hoe_icon_list.draw(pixelated=True)

            arcade.draw_text(
                "Курсор",
                self.cursor_icon.center_x - 28,
                y + 38,
                (255, 255, 255, text_alpha),
                15
            )

            arcade.draw_text(
                "Мотыга",
                self.hoe_icon.center_x - 28,
                y + 38,
                (255, 255, 255, text_alpha),
                15
            )

        # Курсор поверх интерфейса
        self.pointer_list.draw(pixelated=True)
