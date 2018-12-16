import tkinter
import random

# Направления движения змейки соответствуют кодам клавишь
DIRECTION_LEFT = 37
DIRECTION_RIGHT = 39
DIRECTION_UP = 38
DIRECTION_DOWN = 40

# Группы направлений
DIRECTIONS_HORIZONTAL = (DIRECTION_RIGHT, DIRECTION_LEFT,)
DIRECTIONS_VERTICAL = (DIRECTION_UP, DIRECTION_DOWN,)
DIRECTIONS_ALL = DIRECTIONS_HORIZONTAL + DIRECTIONS_VERTICAL

FIELD_WIDTH = 15
FIELD_HEIGHT = 15
BLOCK_SIZE = 25

GAME_SPEED = 1000 // 8  # Количество клеток, которые проходит змейка за 1 секунду

COLORS = {
    'SNAKE_BODY': '#cddc39',
    'SNAKE_HEAD': '#e58d51',
    'FRUIT': '#e05170',
    'FIELD': '#37474f',
    'FIELD_LINE': '#3a4c54',
    'MESSAGE_TEXT': '#ffffff',
    'MESSAGE_BACKGROUND': '#000000'
}


class Snake:
    body = None
    _direction = DIRECTION_LEFT
    _grow = False
    _is_bump = False

    def __init__(self, field_width, field_height):
        """
        Метод инициализации змейки
        :param field_width: int - ширина игрового поля в клетках
        :param field_height: int - высота игрового поля в клетках
        """
        self.field_width = field_width
        self.field_height = field_height
        # Генерация тела змейки
        self.body = [(x, self.field_height // 2) for x in range(self.field_width // 2 - 1, self.field_width // 2 + 2)]

    def get_head(self):
        """
        Метод получения головы змейки
        :return: tuple of int - координаты головы змейки в игровом поле
        """
        return self.body[0]

    def set_direction(self, direction):
        """
        Метод установки направления движения змейки
        :param direction: константа направления
        """
        new_direction = direction
        old_direction = self._direction
        if new_direction in DIRECTIONS_HORIZONTAL and old_direction not in DIRECTIONS_HORIZONTAL:
            self._direction = new_direction
        elif new_direction in DIRECTIONS_VERTICAL and old_direction not in DIRECTIONS_VERTICAL:
            self._direction = new_direction

    def grow(self):
        """
        Метод заставляет змейку расти
        """
        self._grow = True

    def move(self):
        """
        Метод движения змейки по игровому полю
        """
        head = self.get_head()
        # Перемещение головы в другую клетку
        if self._direction == DIRECTION_LEFT:
            head = (head[0] - 1, head[1])
        elif self._direction == DIRECTION_RIGHT:
            head = (head[0] + 1, head[1])
        elif self._direction == DIRECTION_UP:
            head = (head[0], head[1] - 1)
        elif self._direction == DIRECTION_DOWN:
            head = (head[0], head[1] + 1)
        # Перемещение тела змеийки
        if self._grow:
            body = [head] + self.body
            self._grow = False
        else:
            body = [head] + self.body[:-1]
        # Проверка столкновений змейки с границами поля или со своим телом
        bump_yourself = head in body[1:]
        bump_wall = not (0 <= head[0] < self.field_width) or not (0 <= head[1] < self.field_height)
        if bump_yourself or bump_wall:  # Если столкновение было
            self._is_bump = True
        else:  # Если столкновений не было, то перемещения змейки вступают в силу
            self.body = body

    def is_bump(self):
        """
        Метод для проверки было ли столкновение змейки с препятствиями
        :return: bool - True, если столкновение было и False, если столкновения не было
        """
        return self._is_bump
            

class Fruit:
    x = None
    y = None

    def __init__(self, snake, field_width, field_height):
        """
        Метод инициализации фрукта
        :param snake: list of tuple - тело змейки
        :param field_width: int - ширина игрового поля в клетках
        :param field_height: int - высота игрового поля в клетках
        """
        self.field_width = field_width
        self.field_height = field_height
        self.random_new_position(snake=snake)

    def random_new_position(self, snake):
        """
        Метод генерации места в котором будет находиться фрукт
        :param snake: змейка
        """
        all_positions = set()
        for x in range(self.field_width):
            for y in range(self.field_height):
                all_positions.add((x, y))
        snake_positions = set(snake.body)
        possible_positions = list(all_positions - snake_positions)
        position = random.choice(possible_positions)
        self.x = position[0]
        self.y = position[1]

    def is_eaten(self, snake_head):
        """
        Метод проверяет был ли фрукт съеден
        :param snake_head: голова змейки (кортеж с координатами)
        :return: bool - True если фрукт съеден, иначе False
        """
        return snake_head == (self.x, self.y)


class Game:
    """
    Класс игры. Отвечает за обработку пользовательского ввода,
    отрисовку игровой сцены и игровую логику.
    """
    snake = None
    fruit = None
    is_stop = True
    pressed_key = None

    def __init__(self, master, field_width=FIELD_WIDTH, field_height=FIELD_HEIGHT, block_size=BLOCK_SIZE):
        """
        Метод инициализации игрового объекта
        :param master: окно в котором будет отображаться игра
        :param field_width: int - ширина игрового поля в клетках
        :param field_height: int - высота игрового поля в клетках
        :param block_size: int - размер клетки игрового поля в пикселях
        """
        self.master = master
        # Запоминаем переданные параметры игрового поля
        self.field_width = field_width
        self.field_height = field_height
        self.block_size = block_size
        # Создаём канвас с рассчитанными размерами
        self.canvas = tkinter.Canvas(master, width=field_width * block_size, height=field_height * block_size)
        self.canvas.pack()
        # Привязываем обработку нажатий клавищь к методу
        master.bind('<KeyPress>', self.key_press)

    def initialize(self):
        """
        Метод инициализации игровых сущностей
        """
        self.pressed_key = None
        self.snake = Snake(field_width=self.field_width, field_height=self.field_height)
        self.fruit = Fruit(snake=self.snake, field_width=self.field_width, field_height=self.field_height)

    def start(self):
        """
        Метод начала игры
        """
        # Инициализируем игровые сущности
        self.initialize()
        # Вызываем первый игровой цикл
        self.update()

    def update(self):
        """
        Метод обновляющий состояние игры
        """
        self.draw()  # Рисуем сцену

        if not self.is_stop:  # Если игра не остановлена
            if self.pressed_key:  # Если была нажата клавиша
                self.snake.set_direction(self.pressed_key)  # Устанавливаем направление змейке
            self.snake.move()

            if self.fruit.is_eaten(snake_head=self.snake.get_head()):  # Если фрукт съеден
                self.fruit.random_new_position(snake=self.snake)  # Заставляем фрукт появиться в другом месте
                self.snake.grow()  # Заставляем змею расти в длину
            if self.snake.is_bump():  # Если змея ударилась об препятствие
                self.is_stop = True  # Завершаем на этом игровой цикл

        self.master.after(GAME_SPEED, self.update)  # Если всё хорошо, то продолжаем игровой цикл

    def key_press(self, event):
        """
        Метод обработки нажатий клавишь
        """
        if self.is_stop:  # Если игра остановлена
            if self.snake and self.snake.is_bump():  # Если игра была остановлена по причине того, что змея ударилась
                self.initialize()  # Пересоздаём змейку и фрукт
            else:
                self.is_stop = False  # Останавливаем или продолжаем игру
        elif event.keycode in DIRECTIONS_ALL:  # Если нажата клавиша указывающая направления
            self.pressed_key = event.keycode  # Запоминаем эту клавишу

    def draw(self):
        """
        Метод для отрисовки игровой сцены
        """
        c = self.canvas
        # Очищаем экран
        c.delete('all')

        # Рисуем поле
        c.create_rectangle(0, 0, self.field_width * self.block_size, self.field_height * self.block_size,
                           fill=COLORS['FIELD'], width=0)
        # Рисуем вертикальные линии на поле
        for i in range(self.field_width):
            c.create_line(i * self.block_size, 0,
                          i * self.block_size, self.field_height * self.block_size,
                          fill=COLORS['FIELD_LINE'], width=1)
        # Рисуем горизонтальные линии на поле
        for i in range(self.field_height):
            c.create_line(0, i * self.block_size,
                          self.field_width * self.block_size, i * self.block_size,
                          fill=COLORS['FIELD_LINE'], width=1)

        # Рисуем голову змейки
        x, y = self.snake.get_head()
        c.create_rectangle(x * self.block_size, y * self.block_size,
                           x * self.block_size + self.block_size, y * self.block_size + self.block_size,
                           fill=COLORS['SNAKE_HEAD'], width=0)
        # Рисуем тело змейки
        for x, y in self.snake.body[1:]:
            c.create_rectangle(x * self.block_size, y * self.block_size,
                               x * self.block_size + self.block_size, y * self.block_size + self.block_size,
                               fill=COLORS['SNAKE_BODY'], width=0)
        # Рисуем фрукт
        c.create_oval(self.fruit.x * self.block_size,
                      self.fruit.y * self.block_size,
                      self.fruit.x * self.block_size + self.block_size,
                      self.fruit.y * self.block_size + self.block_size,
                      fill=COLORS['FRUIT'], width=0)
        # Если игра остановлена выводим сообщение для игрока
        if self.is_stop:
            c.create_rectangle(0, self.field_height * self.block_size / 3,
                               self.field_width * self.block_size, self.field_height * self.block_size / 3 * 2,
                               fill=COLORS['MESSAGE_BACKGROUND'], width=0, stipple='gray25')
            c.create_text(self.field_width * self.block_size / 2, self.field_height * self.block_size / 2,
                          text="Press any key to start", justify=tkinter.CENTER,
                          font="Monaco %d bold" % (self.block_size * 0.7), fill=COLORS['MESSAGE_TEXT'])


def main():
    root = tkinter.Tk()
    root.title('Snake Game')
    Game(root).start()
    root.mainloop()


if __name__ == '__main__':
    main()
