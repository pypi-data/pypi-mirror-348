class Calculator:
    def __init__(self, name="Simple Calculator"):
        self.name = name
        self.result = 0
        self.history = []
    
    def add(self, a, b):
        """Add two numbers and return the result."""
        self.result = a + b
        self.history.append(f"{a} + {b} = {self.result}")
        return self.result
    
    def subtract(self, a, b):
        """Subtract b from a and return the result."""
        self.result = a - b
        self.history.append(f"{a} - {b} = {self.result}")
        return self.result
    
    def multiply(self, a, b):
        """Multiply two numbers and return the result."""
        self.result = a * b
        self.history.append(f"{a} * {b} = {self.result}")
        return self.result
    
    def divide(self, a, b):
        """Divide a by b and return the result."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        self.result = a / b
        self.history.append(f"{a} / {b} = {self.result}")
        return self.result
        
    def get_result(self):
        """Return the current result."""
        return self.result
    
    def get_history(self):
        """Return the calculation history."""
        return self.history


# Example usage
if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(5, 3))       # 8
    print(calc.subtract(10, 4)) # 6
    print(calc.multiply(3, 4))  # 12
    print(calc.divide(10, 2))   # 5.0
    print(calc.get_history())   # List of operations
