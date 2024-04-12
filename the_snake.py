from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# RGB константы:
BOARD_BACKGROUND_COLOR = (100, 100, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (5, 255, 5)

# FPS:
SPEED = 20

# Screen setup:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс"""

    def __init__(self, body_color=None):
        """Инициализация атрибутов базового класса"""
        self.position = CENTER_POSITION
        self.body_color = body_color

    def draw(self):
        """
        Болванка метода для отрисовки
        производными классами своих объектов
        """
        pass


class Apple(GameObject):
    """Производный класс, наследующий от базового класса (яблоко)"""

    def __init__(self):
        """Инициализация атрибутов производного класса"""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """
        Метод производного класса для установки объекта
        в случайном месте игровой поверхности
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод отрисовки объекта производного класса (яблоко)"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Производный класс, наследующий от базового класса (змея)"""

    def __init__(self):
        """Инициализация атрибутов производного класса"""
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.position = CENTER_POSITION
        self.positions = [self.position]
        self.length = 1

    def draw(self, surface):
        """Метод отрисовки объекта производного класса (змея)"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        for position in self.positions:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возврата головы змеи"""
        return self.positions[0]

    def move(self):
        """Метод движения объекта (змея)"""
        head_position = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (
            (head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if new_head_position in self.positions[1:]:
            self.reset()
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def update_direction(self):
        """Метод для обновления движения объекта (змея)"""
        if self.next_direction:
            self.direction = self.next_direction

    def reset(self):
        """Метод для обновления объекта (змея)"""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice(DIRECTIONS)
        self.next_direction = None


def handle_keys(game_object):
    """Метод управления внутриигровыми событиями"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главный метод игры"""
    snake = Snake()
    apple = Apple()

    while True:
        """Бесконечный цикл игрового процесса (логика игры)"""
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position()
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
