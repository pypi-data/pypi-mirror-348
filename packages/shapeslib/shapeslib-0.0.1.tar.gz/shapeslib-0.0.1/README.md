# ShapesLib

Библиотека для вычисления площади геометрических фигур.

## Установка

```bash
pip install shapeslib
```

## Использование

### Круг
```python
from shapeslib import Circle

circle = Circle(5)
print(circle.area())  # 78.53981633974483
```

### Треугольник
```python
from shapeslib import Triangle

triangle = Triangle(3, 4, 5)
print(triangle.area())  # 6.0
print(triangle.is_right_angled())  # True
```

### Общий расчет площади
```python
from shapeslib import calculate_area, Circle, Triangle

print(calculate_area(Circle(2)))  # 12.566370614359172
print(calculate_area(Triangle(5, 5, 5)))  # 10.825317547305483
```