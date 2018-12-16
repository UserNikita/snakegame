import unittest

from snake import Fruit, Snake


class FruitTests(unittest.TestCase):
    def test_position_random_left_bottom(self):
        """
        # | 1 | 2 |
        # | _ | 3 |
        """
        snake = Snake(field_width=2, field_height=2)
        snake.body = [(0, 0), (1, 0), (1, 1)]
        fruit = Fruit(snake, field_width=2, field_height=2)
        self.assertEqual(fruit.x, 0)
        self.assertEqual(fruit.y, 1)

    def test_position_random_left_top(self):
        """
        # | _ | 1 |
        # | 3 | 2 |
        """
        snake = Snake(field_width=2, field_height=2)
        snake.body = [(1, 0), (1, 1), (0, 1)]
        fruit = Fruit(snake, field_width=2, field_height=2)
        self.assertEqual(fruit.x, 0)
        self.assertEqual(fruit.y, 0)

    def test_position_random_right_bottom(self):
        """
        # | 2 | 3 |
        # | 1 | _ |
        """
        snake = Snake(field_width=2, field_height=2)
        snake.body = [(0, 1), (0, 0), (1, 0)]
        fruit = Fruit(snake, field_width=2, field_height=2)
        self.assertEqual(fruit.x, 1)
        self.assertEqual(fruit.y, 1)

    def test_position_random_right_top(self):
        """
        # | 3 | _ |
        # | 2 | 1 |
        """
        snake = Snake(field_width=2, field_height=2)
        snake.body = [(1, 1), (0, 1), (0, 0)]
        fruit = Fruit(snake, field_width=2, field_height=2)
        self.assertEqual(fruit.x, 1)
        self.assertEqual(fruit.y, 0)


if __name__ == '__main__':
    unittest.main()
