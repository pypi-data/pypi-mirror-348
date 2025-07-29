import sys
import math
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from shapeslib.shape import Circle, Triangle, calculate_area


class TestShapes(unittest.TestCase):
    def test_circle_area(self):
        circle = Circle(1)
        self.assertAlmostEqual(circle.area(), math.pi)
        
        circle = Circle(2)
        self.assertAlmostEqual(circle.area(), math.pi * 4)
    
    def test_circle_invalid_radius(self):
        with self.assertRaises(ValueError):
            Circle(-1)
        with self.assertRaises(ValueError):
            Circle(0)
    
    def test_triangle_area(self):
        triangle = Triangle(3, 4, 5)
        self.assertAlmostEqual(triangle.area(), 6.0)
        
        triangle = Triangle(5, 5, 5)
        self.assertAlmostEqual(triangle.area(), 10.825317547305483)
    
    def test_triangle_invalid_sides(self):
        with self.assertRaises(ValueError):
            Triangle(1, 1, 3)
        
        with self.assertRaises(ValueError):
            Triangle(-1, 2, 2)
    
    def test_right_angled_triangle(self):
        self.assertTrue(Triangle(3, 4, 5).is_right_angled())
        self.assertTrue(Triangle(5, 12, 13).is_right_angled())
        self.assertFalse(Triangle(5, 5, 5).is_right_angled())
    
    def test_calculate_area(self):
        self.assertAlmostEqual(calculate_area(Circle(1)), math.pi)
        self.assertAlmostEqual(calculate_area(Triangle(3, 4, 5)), 6.0)

if __name__ == "__main__":
    unittest.main()