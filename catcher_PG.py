import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Параметры корзины
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
BASKET_SPEED = 7
BASKET_Y = SCREEN_HEIGHT - BASKET_HEIGHT - 10  # Отступ снизу

# Параметры падающего объекта
OBJECT_SIZE = 15  # квадрат 15x15
OBJECT_SPEED = 5

# Условие окончания игры
MAX_MISSES = 5  # N пропусков для завершения игры

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ловец предметов")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Игровые переменные
basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
score = 0
misses = 0

# Падающий объект (прямоугольник)
object_x = random.randint(0, SCREEN_WIDTH - OBJECT_SIZE)
object_y = 0

# Функция отображения текста
def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Управление корзиной (клавиши A/D или стрелки)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        basket_x -= BASKET_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        basket_x += BASKET_SPEED

    # Границы для корзины
    if basket_x < 0:
        basket_x = 0
    if basket_x > SCREEN_WIDTH - BASKET_WIDTH:
        basket_x = SCREEN_WIDTH - BASKET_WIDTH

    # Движение падающего объекта
    object_y += OBJECT_SPEED

    # Проверка столкновения (прямоугольник с прямоугольником)
    basket_rect = pygame.Rect(basket_x, BASKET_Y, BASKET_WIDTH, BASKET_HEIGHT)
    object_rect = pygame.Rect(object_x, object_y, OBJECT_SIZE, OBJECT_SIZE)

    if basket_rect.colliderect(object_rect):
        # Поймали предмет
        score += 1
        # Перемещаем объект наверх со случайной позицией по X
        object_x = random.randint(0, SCREEN_WIDTH - OBJECT_SIZE)
        object_y = 0

    # Проверка, упал ли объект (ниже экрана)
    if object_y > SCREEN_HEIGHT:
        misses += 1
        # Перемещаем объект наверх со случайной позицией
        object_x = random.randint(0, SCREEN_WIDTH - OBJECT_SIZE)
        object_y = 0

    # Условие окончания игры
    if misses >= MAX_MISSES:
        running = False

    # Отрисовка
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (basket_x, BASKET_Y, BASKET_WIDTH, BASKET_HEIGHT))
    pygame.draw.rect(screen, RED, (object_x, object_y, OBJECT_SIZE, OBJECT_SIZE))

    # Отображение счёта и пропусков
    draw_text(f"Счёт: {score}", WHITE, 10, 10)
    draw_text(f"Пропущено: {misses}/{MAX_MISSES}", WHITE, 10, 50)

    pygame.display.flip()
    clock.tick(FPS)

# Экран окончания игры
screen.fill(BLACK)
draw_text("ИГРА ОКОНЧЕНА!", WHITE, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50)
draw_text(f"Ваш счёт: {score}", WHITE, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2)
draw_text("Нажмите любую клавишу для выхода", WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50)
pygame.display.flip()

# Ожидание нажатия клавиши перед выходом
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
sys.exit()