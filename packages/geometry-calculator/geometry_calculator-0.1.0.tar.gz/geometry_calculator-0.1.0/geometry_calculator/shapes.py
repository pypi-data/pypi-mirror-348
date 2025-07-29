import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Абстрактный базовый класс для геометрических фигур"""

    @abstractmethod
    def area(self) -> float:
        """Вычисляет площадь фигуры"""
        pass

    @abstractmethod
    def is_right_angled(self) -> bool:
        """Проверяет, является ли фигура прямоугольной (если применимо)"""
        pass


class Circle(Shape):
    """Класс для представления круга"""

    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным числом")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius**2

    def is_right_angled(self) -> bool:
        return False


class Triangle(Shape):
    """Класс для представления треугольника"""

    def __init__(self, a: float, b: float, c: float):
        sides = [a, b, c]
        if any(side <= 0 for side in sides):
            raise ValueError("Все стороны должны быть положительными числами")
        if not self._is_valid_triangle(a, b, c):
            raise ValueError("Треугольник с такими сторонами не существует")
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        # Формула Герона с кэшированием
        p = (self.a + self.b + self.c) / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def is_right_angled(self, tolerance: float = 1e-6) -> bool:
        sides = sorted([self.a, self.b, self.c])
        return abs(sides[0] ** 2 + sides[1] ** 2 - sides[2] ** 2) < tolerance

    @staticmethod
    def _is_valid_triangle(a: float, b: float, c: float) -> bool:
        return (a + b > c) and (a + c > b) and (b + c > a)


def calculate_area(shape: Shape) -> float:
    """Вычисляет площадь фигуры без знания её типа в compile-time"""
    return shape.area()


def is_right_angled(shape: Shape) -> bool:
    """Проверяет, является ли фигура прямоугольной"""
    return shape.is_right_angled()
