class Shape:
    def __init__(self, name):
        self.name = name
    
    def area(self):
        # This method should be overridden by subclasses
        raise NotImplementedError("Subclasses must implement area()")
    
    def perimeter(self):
        # This method should be overridden by subclasses
        raise NotImplementedError("Subclasses must implement perimeter()")
    
    def __str__(self):
        return self.name

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return f"{self.name}(width={self.width}, height={self.height})"

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius
    
    def __str__(self):
        return f"{self.name}(radius={self.radius})"

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.name = "Square"
    
    def __str__(self):
        return f"{self.name}(side={self.width})"

def main():
    shapes = [
        Rectangle(5, 10),
        Circle(7),
        Square(4)
    ]
    
    for shape in shapes:
        print(f"{shape} - Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")

if __name__ == "__main__":
    main()
