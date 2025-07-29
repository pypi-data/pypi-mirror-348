def process_data(data):
    """Process the input data and return the result."""
    result = data * 2
    return result

def main():
    input_data = [1, 2, 3, 4, 5]
    output = process_data(input_data)
    print(f"Input: {input_data}")
    print(f"Output: {output}")

if __name__ == "__main__":
    main()
