import tkinter as tk
import random
import math

# Константы
WIDTH = 800
HEIGHT = 600
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
ITEM_SIZE = 25
MAX_MISSES = 25  # N пропусков для окончания игры
INITIAL_FALL_SPEED = 1
SPEED_INCREMENT = 0.1  # Ускорение со временем
SPEED_INCREMENT_INTERVAL = 5000  # Интервал увеличения скорости (мс)
SPAWN_INTERVAL = 100  # Интервал спавна новых предметов (кадры)

# Цвета
COLORS = {
    'bg': '#1a1a2e',
    'basket': '#3498db',
    'basket_border': '#ecf0f1',
    'item1': '#f1c40f',  # Звезда
    'item2': '#00ffff',  # Кристалл
    'item3': '#e74c3c',  # Сердце
    'item4': '#e67e22',  # Монета
    'item5': '#9b59b6',  # Алмаз
    'text': '#ffffff',
    'text_shadow': '#000000',
    'miss_bar_bg': '#34495e',
    'miss_bar_fg': '#e74c3c',
}


class FallingItem:
    """Класс падающего предмета"""

    # Типы предметов
    ITEM_TYPES = {
        1: {'name': 'Звезда', 'color': COLORS['item1'], 'points': 10, 'shape': 'star'},
        2: {'name': 'Кристалл', 'color': COLORS['item2'], 'points': 20, 'shape': 'crystal'},
        3: {'name': 'Сердце', 'color': COLORS['item3'], 'points': 30, 'shape': 'heart'},
        4: {'name': 'Монета', 'color': COLORS['item4'], 'points': 15, 'shape': 'circle'},
        5: {'name': 'Алмаз', 'color': COLORS['item5'], 'points': 50, 'shape': 'diamond'},
    }

    def __init__(self, canvas, item_type=None, fall_speed=INITIAL_FALL_SPEED):
        self.canvas = canvas
        self.fall_speed = fall_speed

        if item_type is None:
            self.type = random.choice(list(self.ITEM_TYPES.keys()))
        else:
            self.type = item_type

        self.data = self.ITEM_TYPES[self.type]
        self.x = random.randint(ITEM_SIZE, WIDTH - ITEM_SIZE)
        self.y = -ITEM_SIZE
        self.id = None
        self.create_item()

    def create_item(self):
        """Создание предмета на canvas"""
        shape = self.data['shape']
        color = self.data['color']
        x1, y1 = self.x - ITEM_SIZE // 2, self.y
        x2, y2 = self.x + ITEM_SIZE // 2, self.y + ITEM_SIZE

        if shape == 'star':
            # Рисуем звезду
            points = []
            cx, cy = self.x, self.y + ITEM_SIZE // 2
            outer_r = ITEM_SIZE // 2
            inner_r = ITEM_SIZE // 4

            for i in range(5):
                angle = (i * 72 - 90) * math.pi / 180
                x_outer = cx + outer_r * math.cos(angle)
                y_outer = cy + outer_r * math.sin(angle)
                points.extend([x_outer, y_outer])

                angle = ((i * 72 + 36) - 90) * math.pi / 180
                x_inner = cx + inner_r * math.cos(angle)
                y_inner = cy + inner_r * math.sin(angle)
                points.extend([x_inner, y_inner])

            self.id = self.canvas.create_polygon(points, fill=color, outline='white', width=1)

        elif shape == 'crystal':
            # Рисуем кристалл
            cx, cy = self.x, self.y + ITEM_SIZE // 2
            points = [
                cx, cy - ITEM_SIZE // 2,
                    cx + ITEM_SIZE // 2, cy,
                cx, cy + ITEM_SIZE // 2,
                    cx - ITEM_SIZE // 2, cy
            ]
            self.id = self.canvas.create_polygon(points, fill=color, outline='white', width=1)

        elif shape == 'heart':
            # Рисуем сердце
            cx, cy = self.x, self.y + ITEM_SIZE // 2
            points = []
            for t in range(0, 360, 10):
                rad = t * math.pi / 180
                x = cx + 16 * math.sin(rad) ** 3
                y = cy - (13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad))
                points.extend([x, y])
            self.id = self.canvas.create_polygon(points, fill=color, outline='white', width=1, smooth=True)

        elif shape == 'circle':
            # Рисуем монету
            cx, cy = self.x, self.y + ITEM_SIZE // 2
            self.id = self.canvas.create_oval(
                cx - ITEM_SIZE // 2, cy - ITEM_SIZE // 2,
                cx + ITEM_SIZE // 2, cy + ITEM_SIZE // 2,
                fill=color, outline='gold', width=2
            )
            # Добавляем символ $
            self.canvas.create_text(cx, cy, text='$', fill='gold', font=('Arial', 12, 'bold'), tags=(self.id,))

        else:  # diamond
            # Рисуем алмаз
            cx, cy = self.x, self.y + ITEM_SIZE // 2
            points = [
                cx, cy - ITEM_SIZE // 2,
                    cx + ITEM_SIZE // 2, cy,
                cx, cy + ITEM_SIZE // 2,
                    cx - ITEM_SIZE // 2, cy
            ]
            self.id = self.canvas.create_polygon(points, fill=color, outline='white', width=2)
            # Добавляем блеск
            self.canvas.create_line(cx, cy - ITEM_SIZE // 2, cx, cy, fill='white', width=1, tags=(self.id,))

    def move(self):
        """Перемещение предмета вниз"""
        self.y += self.fall_speed
        self.canvas.move(self.id, 0, self.fall_speed)
        # Перемещаем связанные элементы (текст и линии)
        for item in self.canvas.find_withtag(self.id):
            if item != self.id:
                self.canvas.move(item, 0, self.fall_speed)

    def get_position(self):
        """Получение позиции предмета"""
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        return x1, y1, x2, y2

    def is_off_screen(self):
        """Проверка, вышел ли предмет за экран"""
        _, y1, _, _ = self.get_position()
        return y1 > HEIGHT

    def delete(self):
        """Удаление предмета"""
        for item in self.canvas.find_withtag(self.id):
            self.canvas.delete(item)


class Basket:
    """Класс корзины"""

    def __init__(self, canvas):
        self.canvas = canvas
        self.width = BASKET_WIDTH
        self.height = BASKET_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 15
        self.id = None
        self.create_basket()

    def create_basket(self):
        """Создание корзины на canvas"""
        # Основной прямоугольник
        self.id = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill=COLORS['basket'], outline=COLORS['basket_border'], width=2
        )
        # Ручка корзины
        handle_width = self.width // 2
        self.canvas.create_arc(
            self.x + self.width // 4, self.y - 15,
            self.x + self.width // 4 + handle_width, self.y + 5,
            start=0, extent=180, outline=COLORS['basket_border'], width=2, style=tk.ARC
        )

    def move_left(self):
        """Движение влево"""
        if self.x > 0:
            self.x -= self.speed
            self.canvas.move(self.id, -self.speed, 0)

    def move_right(self):
        """Движение вправо"""
        if self.x < WIDTH - self.width:
            self.x += self.speed
            self.canvas.move(self.id, self.speed, 0)

    def get_position(self):
        """Получение позиции корзины"""
        return self.canvas.bbox(self.id)

    def update_position(self):
        """Обновление позиции после сброса"""
        self.x = WIDTH // 2 - self.width // 2
        self.canvas.coords(self.id, self.x, self.y, self.x + self.width, self.y + self.height)


class CatcherGame:
    """Основной класс игры"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ловец предметов")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS['bg'])

        # Создание canvas
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=COLORS['bg'], highlightthickness=0)
        self.canvas.pack()

        # Игровые переменные
        self.score = 0
        self.misses = 0
        self.fall_speed = INITIAL_FALL_SPEED
        self.game_over = False
        self.paused = False
        self.items = []
        self.combo = 0
        self.combo_timer = 0
        self.spawn_counter = 0

        # Создание объектов
        self.basket = Basket(self.canvas)

        # Текст для отображения счета
        self.score_text = self.canvas.create_text(20, 20, anchor='nw',
                                                  font=('Arial', 20, 'bold'),
                                                  fill=COLORS['text'], text="Счет: 0")
        self.misses_text = self.canvas.create_text(20, 50, anchor='nw',
                                                   font=('Arial', 20, 'bold'),
                                                   fill=COLORS['text'], text=f"Пропуски: 0/{MAX_MISSES}")
        self.speed_text = self.canvas.create_text(20, 80, anchor='nw',
                                                  font=('Arial', 16),
                                                  fill=COLORS['item2'], text=f"Скорость: {self.fall_speed:.1f}")
        self.combo_text = self.canvas.create_text(20, 110, anchor='nw',
                                                  font=('Arial', 16, 'bold'),
                                                  fill=COLORS['item1'], text="")

        # Полоса пропусков
        self.miss_bar_bg = self.canvas.create_rectangle(
            WIDTH - 220, 20, WIDTH - 20, 40,
            fill=COLORS['miss_bar_bg'], outline=''
        )
        self.miss_bar_fg = self.canvas.create_rectangle(
            WIDTH - 220, 20, WIDTH - 220, 40,
            fill=COLORS['miss_bar_fg'], outline=''
        )

        # Привязка клавиш
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<a>', self.move_left)
        self.root.bind('<d>', self.move_right)
        self.root.bind('<p>', self.toggle_pause)
        self.root.bind('<r>', self.restart_game)
        self.root.bind('<Escape>', self.quit_game)

        # Фокус на окно для захвата клавиш
        self.canvas.focus_set()

        # Таймер для увеличения скорости
        self.last_speed_increase = self.root.after(0, self.increase_speed)
        self.speed_increase_id = None

        # Создание начальных предметов
        for _ in range(3):
            self.spawn_item()

        # Запуск игрового цикла
        self.game_loop()

        # Запуск таймера увеличения скорости
        self.start_speed_increase()

        self.root.mainloop()

    def move_left(self, event=None):
        """Движение корзины влево"""
        if not self.game_over and not self.paused:
            self.basket.move_left()

    def move_right(self, event=None):
        """Движение корзины вправо"""
        if not self.game_over and not self.paused:
            self.basket.move_right()

    def toggle_pause(self, event=None):
        """Пауза"""
        if not self.game_over:
            self.paused = not self.paused
            if not self.paused:
                self.canvas.focus_set()

    def restart_game(self, event=None):
        """Перезапуск игры"""
        if self.game_over:
            # Очистка всех предметов
            for item in self.items:
                item.delete()
            self.items.clear()

            # Сброс переменных
            self.score = 0
            self.misses = 0
            self.fall_speed = INITIAL_FALL_SPEED
            self.game_over = False
            self.paused = False
            self.combo = 0
            self.combo_timer = 0
            self.spawn_counter = 0

            # Обновление корзины
            self.basket.update_position()

            # Обновление текста
            self.update_ui()

            # Создание новых предметов
            for _ in range(3):
                self.spawn_item()

            # Перезапуск таймера скорости
            if self.speed_increase_id:
                self.root.after_cancel(self.speed_increase_id)
            self.start_speed_increase()

            self.canvas.focus_set()

    def quit_game(self, event=None):
        """Выход из игры"""
        self.root.quit()

    def start_speed_increase(self):
        """Запуск таймера увеличения скорости"""
        self.speed_increase_id = self.root.after(SPEED_INCREMENT_INTERVAL, self.increase_speed)

    def increase_speed(self):
        """Увеличение скорости падения"""
        if not self.game_over and not self.paused:
            self.fall_speed += SPEED_INCREMENT
            self.update_ui()
        self.speed_increase_id = self.root.after(SPEED_INCREMENT_INTERVAL, self.increase_speed)

    def spawn_item(self):
        """Создание нового предмета"""
        # Чем больше очков, тем чаще ценные предметы
        if random.random() < 0.3 + self.score / 5000:
            item_type = random.choice([2, 3, 5])
        else:
            item_type = random.choice([1, 4])

        self.items.append(FallingItem(self.canvas, item_type, self.fall_speed))

    def check_collision(self, item):
        """Проверка столкновения предмета с корзиной"""
        item_x1, item_y1, item_x2, item_y2 = item.get_position()
        basket_x1, basket_y1, basket_x2, basket_y2 = self.basket.get_position()

        return (item_x2 > basket_x1 and item_x1 < basket_x2 and
                item_y2 > basket_y1 and item_y1 < basket_y2)

    def catch_item(self, item):
        """Обработка поимки предмета"""
        # Начисление очков с учетом комбо
        points = item.data['points'] * (1 + self.combo * 0.1)
        self.score += int(points)

        # Увеличение комбо
        self.combo += 1
        self.combo_timer = 30  # Комбо держится ~0.5 секунды

        # Создание эффекта частиц
        self.create_particles(item)

        # Удаление предмета
        item.delete()
        self.items.remove(item)

        # Создание нового предмета
        self.spawn_item()

        self.update_ui()

    def miss_item(self, item):
        """Обработка пропуска предмета"""
        self.misses += 1
        self.combo = 0  # Сброс комбо при пропуске

        # Удаление предмета
        item.delete()
        self.items.remove(item)

        # Создание нового предмета
        self.spawn_item()

        self.update_ui()

        # Проверка окончания игры
        if self.misses >= MAX_MISSES:
            self.game_over = True
            self.show_game_over()

    def create_particles(self, item):
        """Создание эффекта частиц при ловле"""
        x1, y1, x2, y2 = item.get_position()
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        color = item.data['color']

        # Создание нескольких маленьких кружков
        particles = []
        for _ in range(10):
            particle = self.canvas.create_oval(
                cx - 3, cy - 3, cx + 3, cy + 3,
                fill=color, outline=''
            )
            particles.append(particle)

        # Анимация частиц
        def animate_particles(particles, step=0):
            if step < 20 and not self.game_over:
                for p in particles:
                    self.canvas.move(p, random.randint(-5, 5), random.randint(-10, -2))
                self.root.after(50, lambda: animate_particles(particles, step + 1))
            else:
                for p in particles:
                    self.canvas.delete(p)

        animate_particles(particles)

    def update_ui(self):
        """Обновление интерфейса"""
        self.canvas.itemconfig(self.score_text, text=f"Счет: {self.score}")
        self.canvas.itemconfig(self.misses_text, text=f"Пропуски: {self.misses}/{MAX_MISSES}")
        self.canvas.itemconfig(self.speed_text, text=f"Скорость: {self.fall_speed:.1f}")

        # Обновление комбо
        if self.combo > 0:
            self.canvas.itemconfig(self.combo_text, text=f"Комбо: x{self.combo}!")
        else:
            self.canvas.itemconfig(self.combo_text, text="")

        # Обновление полосы пропусков
        miss_width = 200 * (self.misses / MAX_MISSES)
        self.canvas.coords(self.miss_bar_fg, WIDTH - 220, 20, WIDTH - 220 + miss_width, 40)

    def show_game_over(self):
        """Отображение экрана окончания игры"""
        # Полупрозрачный оверлей
        overlay = self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='black', stipple='gray50')

        # Текст Game Over
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 60,
                                text="GAME OVER",
                                font=('Arial', 48, 'bold'),
                                fill=COLORS['item3'])

        # Финальный счет
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2,
                                text=f"Финальный счет: {self.score}",
                                font=('Arial', 24, 'bold'),
                                fill=COLORS['text'])

        # Количество пойманных предметов
        caught = int(self.score / 15)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 50,
                                text=f"Поймано предметов: ~{caught}",
                                font=('Arial', 18),
                                fill=COLORS['item2'])

        # Инструкция по перезапуску
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 110,
                                text="Нажмите R для перезапуска",
                                font=('Arial', 16),
                                fill=COLORS['item1'])

        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 150,
                                text="Нажмите ESC для выхода",
                                font=('Arial', 16),
                                fill=COLORS['item4'])

    def game_loop(self):
        """Основной игровой цикл"""
        if not self.game_over and not self.paused:
            # Обновление комбо таймера
            if self.combo_timer > 0:
                self.combo_timer -= 1
                if self.combo_timer == 0:
                    self.combo = 0
                    self.update_ui()

            # Спавн новых предметов
            self.spawn_counter += 1
            if self.spawn_counter > max(SPAWN_INTERVAL, SPAWN_INTERVAL - int(self.score / 1000)):
                if len(self.items) < 7:  # Ограничение на количество предметов
                    self.spawn_item()
                self.spawn_counter = 0

            # Обновление всех предметов
            for item in self.items[:]:
                item.move()

                # Проверка столкновения
                if self.check_collision(item):
                    self.catch_item(item)
                # Проверка, упал ли предмет
                elif item.is_off_screen():
                    self.miss_item(item)

        # Повторный вызов
        self.root.after(16, self.game_loop)  # ~60 FPS


if __name__ == "__main__":
    game = CatcherGame()


