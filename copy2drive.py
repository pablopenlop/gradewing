import os
import shutil
from datetime import datetime
import math 
# Paths
source_folder = "/Users/teacher/Documents/Django Projects/GRADEBOOK"
drive_folder = "/Users/teacher/Library/CloudStorage/GoogleDrive-pablo.penas@virtuscollege.es/My Drive/Python/GRADEBOOK PROJECT"

# Create a folder with the current date
current_date = datetime.now().strftime('%Y-%m-%d')
destination_folder = os.path.join(drive_folder, current_date)

# Make sure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Function to copy the project while excluding certain directories and files
def copy_project(source, destination):
    total_size = 0  # To keep track of the total size of copied files

    for root, dirs, files in os.walk(source):
        # Exclude .venv, __pycache__, and db.sqlite3, but keep migrations with only __init__.py
        if '.venv' in dirs:
            dirs.remove('.venv')  # Don't walk into .venv
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')  # Don't walk into __pycache__
        
        # Create the corresponding destination folder structure
        dest_dir = os.path.join(destination, os.path.relpath(root, source))
        os.makedirs(dest_dir, exist_ok=True)
        
        # If in a migrations folder, only copy the __init__.py file
        if 'migrations' in root:
            files = [f for f in files if f == '__init__.py']
        else:
            files = [f for f in files if f != 'db.sqlite3']
        
        # Copy files to the destination folder and calculate total size
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dest_file)
            
            # Get the size of the file and add it to the total
            file_size = os.path.getsize(src_file)
            total_size += file_size
            
            print(f"Copied: {src_file} \n --> {dest_file}\n (Size: {file_size} bytes)\n")

    return total_size

# Run the copy function and get total size
total_copied_size = copy_project(source_folder, destination_folder)

# Print total size in a human-readable format (e.g., KB, MB)
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.log(size_bytes, 1024))  # Using math.log for logarithmic calculation
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

print(f"Total size of copied files: {convert_size(total_copied_size)}")
