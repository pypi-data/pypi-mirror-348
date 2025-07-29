class Calculator:
    def __init__(self, name="Simple Calculator"):
        self.name = name
        self.result = 0
    
    def add(self, a, b):
        """Add two numbers and return the result."""
        self.result = a + b
        return self.result
    
    def subtract(self, a, b):
        """Subtract b from a and return the result."""
        self.result = a - b
        return self.result
    
    def reset(self):
        """Reset the calculator result to zero."""
        self.result = 0
        
    def get_result(self):
        """Return the current result."""
        return self.result


# Example usage
if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(5, 3))      # 8
    print(calc.subtract(10, 4)) # 6
    calc.reset()
    print(calc.get_result())   # 0
