import os
import shutil

# Define the path to your Django project directory
project_dir = os.path.dirname(os.path.abspath(__file__))  # Assuming this script is in your project root

def delete_db():
    """Delete the SQLite database file."""
    db_path = os.path.join(project_dir, 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted database: {db_path}")
    else:
        print("No db.sqlite3 found.")

def delete_migrations():
    """Delete all migration files (except __init__.py) from all app migrations folders, excluding '.venv' paths."""
    for root, dirs, files in os.walk(project_dir):
        # Skip any path that contains '.venv'
        if '.venv' in root:
            continue
        if 'migrations' in dirs:
            migrations_dir = os.path.join(root, 'migrations')
            for file in os.listdir(migrations_dir):
                if file != '__init__.py' and file.endswith('.py'):
                    file_path = os.path.join(migrations_dir, file)
                    os.remove(file_path)
                    print(f"Deleted migration: {file_path}")

def delete_pycaches():
    """Delete all __pycache__ directories, excluding paths containing '.venv'."""
    for root, dirs, files in os.walk(project_dir):
        # Skip any path that contains '.venv'
        if '.venv' in root:
            continue
        if '__pycache__' in dirs:
            pycache_dir = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_dir)
            print(f"Deleted __pycache__ directory: {pycache_dir}")

if __name__ == "__main__":
    # Perform the cleanup actions
    delete_db()
    delete_migrations()
    delete_pycaches()
    print("Cleanup complete.")
