import math
from abc import ABC, abstractmethod
from typing import Union

class Shape(ABC):
    """Абстрактный базовый класс для геометрических фигур."""
    
    @abstractmethod
    def area(self) -> float:
        """Вычисляет площадь фигуры."""
        pass
    
    @abstractmethod
    def is_right_angled(self) -> bool:
        """Проверяет, является ли фигура прямоугольной (если применимо)."""
        pass

class Circle(Shape):
    """Класс для представления круга."""
    
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным числом")
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def is_right_angled(self) -> bool:
        """Круг не может быть прямоугольным, всегда возвращает False."""
        return False

class Triangle(Shape):
    """Класс для представления треугольника."""
    
    def __init__(self, side1: float, side2: float, side3: float):
        sides = [side1, side2, side3]
        if any(side <= 0 for side in sides):
            raise ValueError("Все стороны должны быть положительными числами")
        sides.sort()
        if sides[0] + sides[1] <= sides[2]:
            raise ValueError("Треугольник с такими сторонами не существует")
        self.sides = sides
    
    def area(self) -> float:
        a, b, c = self.sides
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    def is_right_angled(self) -> bool:
        """Проверяет, является ли треугольник прямоугольным по теореме Пифагора."""
        a, b, c = self.sides
        return math.isclose(a**2 + b**2, c**2)

def calculate_area(shape: Union[Circle, Triangle]) -> float:
    """Вычисляет площадь фигуры без знания её типа в compile-time."""
    return shape.area()