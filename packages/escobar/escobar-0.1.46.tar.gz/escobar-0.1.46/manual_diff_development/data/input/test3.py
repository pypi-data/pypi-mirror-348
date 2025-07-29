"""
File handling utility functions
"""

def read_file(filename):
    """
    Read the contents of a file and return as a string.
    
    Args:
        filename (str): The path to the file to read
        
    Returns:
        str: The contents of the file
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    with open(filename, 'r') as file:
        return file.read()

def write_file(filename, content):
    """
    Write content to a file.
    
    Args:
        filename (str): The path to the file to write
        content (str): The content to write to the file
        
    Returns:
        bool: True if the write was successful, False otherwise
    """
    try:
        with open(filename, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

def append_file(filename, content):
    """
    Append content to a file.
    
    Args:
        filename (str): The path to the file to append to
        content (str): The content to append to the file
        
    Returns:
        bool: True if the append was successful, False otherwise
    """
    try:
        with open(filename, 'a') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error appending to file: {e}")
        return False
