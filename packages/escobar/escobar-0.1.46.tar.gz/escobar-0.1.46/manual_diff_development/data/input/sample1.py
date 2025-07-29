def calculate_sum(a, b):
    """
    Calculate the sum of two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
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
    return a - b

def main():
    x = 10
    y = 5
    
    print(f"Sum of {x} and {y} is {calculate_sum(x, y)}")
    print(f"Difference between {x} and {y} is {calculate_difference(x, y)}")

if __name__ == "__main__":
    main()
