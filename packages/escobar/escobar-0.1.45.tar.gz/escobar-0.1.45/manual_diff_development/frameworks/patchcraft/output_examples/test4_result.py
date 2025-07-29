def process_data(data):
    """Process the input data and return the result."""
    # Perform multiple operations on the data
    result = []
    for item in data:
        # Double each item
        doubled = item * 2
        # Add to result list
        result.append(doubled)
    return result

def main():
    input_data = [1, 2, 3, 4, 5]
    output = process_data(input_data)
    print(f"Input: {input_data}")
    print(f"Output: {output}")

if __name__ == "__main__":
    main()
