import os

def search_files(directory, search_strings):
    """
    Search through all files in a directory for occurrences of specified strings.

    arguments:
    - directory (str): Directory path to search.
    - search_strings (list): List of strings to search for.

    returns:
    - result (dict): A dictionary containing file names and corresponding matches.
    """
    result = {}

    # ensure the directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return result

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # skip binary files to avoid encoding issues
            if not is_binary(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    matches = find_matches(content, search_strings)

                    if matches:
                        result[file_path] = matches

    return result

def find_matches(content, search_strings):
    """
    Find occurrences of specified strings in content.

    arguments:
    - content (str): The content to search.
    - search_strings (list): List of strings to search for.

    returns:
    - matches (list): List of tuples containing line number and matched string.
    """
    matches = []

    for line_number, line in enumerate(content.split('\n'), start=1):
        for search_string in search_strings:
            if search_string in line:
                matches.append((line_number, line, search_string))

    return matches

def is_binary(file_path):
    """
    Check if a file is binary.

    arguments:
    - file_path (str): The path to the file.

    returns:
    - is_binary (bool): True if the file is binary, False otherwise.
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read(1024)
            return b'\x00' in content
    except Exception as e:
        print(f"Error checking if '{file_path}' is binary: {e}")
        return False

if __name__ == "__main__":
    # grab user input for the directory and search strings
    search_directory = input("Enter the directory to search: ")
    search_strings = input("Enter the search strings (comma-separated): ").split(',')

    # execute search
    result = search_files(search_directory, search_strings)

    # display results
    if result:
        print("\nSearch Results:")
        for file_path, matches in result.items():
            print(f"\nFile: {file_path}")
            for line_number, line, search_string in matches:
                print(f"  Line {line_number}: '{line}' (Matched: '{search_string}')")
    else:
        print("\nNo matching files found.")