import os
import shutil

# --- CONFIGURATION ---
# NOTE: 
# 1. Use a folder you are okay with organizing. Maybe create a test folder first!
# 2. The path should be an absolute path.
#    - Windows example: "C:/Users/YourUser/Downloads"
#    - macOS/Linux example: "/Users/YourUser/Downloads"
SOURCE_FOLDER = "/path/to/your/messy/folder"

# This dictionary maps folder names to the file extensions they should contain.
# You can easily add more! For example, 'Videos': ['.mov', '.mp4']
FILE_TYPE_MAPPINGS = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.sh']
}

def organize_folder(path):
    """
    Scans a folder and organizes files into subdirectories based on their extension.
    Returns a list of messages describing the actions taken.
    """
    messages = []

    # List all items in the source folder
    for filename in os.listdir(path):
        # Construct the full path of the file
        file_path = os.path.join(path, filename)

        # Skip if it's a directory
        if os.path.isdir(file_path):
            continue

        # Get the file extension
        _, file_extension = os.path.splitext(filename)

        # Find the destination folder for this file type
        destination_folder_name = "Other" # Default folder
        for folder_name, extensions in FILE_TYPE_MAPPINGS.items():
            if file_extension.lower() in extensions:
                destination_folder_name = folder_name
                break
        
        # Create the destination folder if it doesn't exist
        destination_path = os.path.join(path, destination_folder_name)
        os.makedirs(destination_path, exist_ok=True)

        # Move the file
        shutil.move(file_path, os.path.join(destination_path, filename))
        messages.append(f"Moved '{filename}' to '{destination_folder_name}'")
    
    return messages

def search_for_file(folder_path, file_name_query):
    """
    Recursively searches for files matching a query in a given folder.
    The search is case-insensitive and matches partial names.
    Returns a list of full paths to the found files.
    """
    found_files = []
    query = file_name_query.lower()

    # os.walk is perfect for recursively walking through a directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if query in file.lower():
                found_files.append(os.path.join(root, file))
    
    return found_files