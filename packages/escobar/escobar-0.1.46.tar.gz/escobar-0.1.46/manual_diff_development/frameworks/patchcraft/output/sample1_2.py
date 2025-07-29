def calculate_sum(a, b):
    """
    Calculate the sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
+    # Ensure we're working with numbers
+    a = float(a)
+    b = float(b)
    return a + b

def calculate_difference(a, b):
    """
    Calculate the difference between two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference between a and b
    """
+    # Ensure we're working with numbers
+    a = float(a)
+    b = float(b)
    return a - b

def calculate_product(a, b):
    """
    Calculate the product of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
+    # Ensure we're working with numbers
+    a = float(a)
+    b = float(b)
    return a * b

+def calculate_division(a, b):
+    """
+    Calculate the division of two numbers.
+
+    Args:
+        a: First number (dividend)
+        b: Second number (divisor)
+
+    Returns:
+        Result of a divided by b
+    """
+    # Ensure we're working with numbers
+    a = float(a)
+    b = float(b)
+
+    # Check for division by zero
+    if b == 0:
+        raise ValueError("Cannot divide by zero")
+
+    return a / b
+
def main():
    x = 10
    y = 5

    print(f"Sum of {x} and {y} is {calculate_sum(x, y)}")
    print(f"Difference between {x} and {y} is {calculate_difference(x, y)}")
    print(f"Product of {x} and {y} is {calculate_product(x, y)}")
+    print(f"Division of {x} by {y} is {calculate_division(x, y)}")

if __name__ == "__main__":
    main()
