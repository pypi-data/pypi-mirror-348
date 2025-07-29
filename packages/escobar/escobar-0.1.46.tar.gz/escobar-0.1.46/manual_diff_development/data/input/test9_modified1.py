"""
Geometric shapes module
This module defines various geometric shapes and their properties.
"""

# Base class for all shapes
class Shape:
    def __init__(self, name):
        # Store the name of the shape
        self.name = name
    
    def area(self):
        # This method should be overridden by subclasses
        raise NotImplementedError("Subclasses must implement area()")
    
    def perimeter(self):
        # This method should be overridden by subclasses
        raise NotImplementedError("Subclasses must implement perimeter()")
    
    def __str__(self):
        return self.name

# Rectangle class - implements a rectangle shape
class Rectangle(Shape):
    def __init__(self, width, height):
        # Call the parent constructor
        super().__init__("Rectangle")
        # Store the dimensions
        self.width = width
        self.height = height
    
    def area(self):
        # Area = width * height
        return self.width * self.height
    
    def perimeter(self):
        # Perimeter = 2 * (width + height)
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return f"{self.name}(width={self.width}, height={self.height})"

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        # Import math module for pi
        import math
        # Area = π * r²
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        # Perimeter = 2 * π * r
        return 2 * math.pi * self.radius
    
    def __str__(self):
        return f"{self.name}(radius={self.radius})"

# Square is a special case of Rectangle where width = height
class Square(Rectangle):
    def __init__(self, side):
        # Initialize as a rectangle with equal sides
        super().__init__(side, side)
        # Override the name
        self.name = "Square"
    
    # No need to override area() or perimeter() as they work the same as Rectangle
    
    def __str__(self):
        return f"{self.name}(side={self.width})"

def main():
    # Create a list of different shapes
    shapes = [
        Rectangle(5, 10),  # width=5, height=10
        Circle(7),         # radius=7
        Square(4)          # side=4
    ]
    
    # Print information about each shape
    for shape in shapes:
        print(f"{shape} - Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")

# Entry point of the program
if __name__ == "__main__":
    main()
