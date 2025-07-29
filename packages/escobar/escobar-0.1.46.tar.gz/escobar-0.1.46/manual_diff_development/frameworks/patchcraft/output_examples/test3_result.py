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

def file_exists(filename):
    """
    Check if a file exists.

    Args:
        filename (str): The path to the file to check

    Returns:
        bool: True if the file exists, False otherwise
    """
    import os
    return os.path.isfile(filename)

def delete_file(filename):
    """
    Delete a file.

    Args:
        filename (str): The path to the file to delete

    Returns:
        bool: True if the file was deleted, False otherwise
    """
    import os
    try:
        os.remove(filename)
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def copy_file(source, destination):
    """
    Copy a file from source to destination.

    Args:
        source (str): The path to the source file
        destination (str): The path to the destination file

    Returns:
        bool: True if the file was copied, False otherwise
    """
    import shutil
    try:
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    test_file = "test.txt"

    # Write to file
    write_file(test_file, "Hello, World!\n")

    # Append to file
    append_file(test_file, "This is a test file.\n")

    # Read from file
    content = read_file(test_file)
    print(f"File content:\n{content}")

    # Check if file exists
    print(f"File exists: {file_exists(test_file)}")

    # Copy file
    copy_file(test_file, "test_copy.txt")

    # Delete file
    delete_file(test_file)
    print(f"File exists after deletion: {file_exists(test_file)}")
