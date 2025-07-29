def process_items(items):
    results = []
    for item in items:
        if item > 0:
            # Process positive items
            processed = item * 2
            results.append(processed)
        else:
            # Skip non-positive items
            continue
    return results

def filter_items(items, condition):
    filtered = []
    for item in items:
        if condition(item):
            filtered.append(item)
    return filtered

def main():
    # Sample data
    data = [-3, -1, 0, 2, 4, 6]
    
    # Process only positive items
    processed = process_items(data)
    print(f"Processed items: {processed}")
    
    # Filter items greater than 3
    filtered = filter_items(data, lambda x: x > 3)
    print(f"Filtered items: {filtered}")

if __name__ == "__main__":
    main()
