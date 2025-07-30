#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import time

def create_project_structure(project_name):
    # Get the absolute path of the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(script_dir, "temp")

    # Check if temp directory exists
    if not os.path.exists(temp_dir):
        print(f"Error: 'temp' directory not found at {temp_dir}")
        sys.exit(1)

    # Create the project directory
    os.makedirs(project_name, exist_ok=True)

    # Copy contents from temp to the new project
    for item in os.listdir(temp_dir):
        source = os.path.join(temp_dir, item)
        destination = os.path.join(project_name, item)

        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)

    print(f"FastAPI project '{project_name}' created successfully!")

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "new":
        print("Usage: fast-create new <project_name>")
        sys.exit(1)

    project_name = sys.argv[2]
    create_project_structure(project_name)

    # Start FastAPI server if main.py exists
    main_file = os.path.join(project_name, "main.py")
    if os.path.exists(main_file):
        print("Migrating the database using alembic...")
        try:
            subprocess.run(["alembic", "init", "alembic"], cwd=project_name, check=True)
            print("Please ensure to edit the alembic.ini  where it says, 'sqlalchemy.url = driver://user:pass@localhost/dbname' with your actusl development database url and alembic/env.py where it says target_metadata = None with your sqlmodel setting. Eg: target_metadata = SQLModel.metadata. Also ensure to import your models to the alembic/env.py to acually migrate the changes. After making sure the target_metadata is correctly configured, you can now try running the --autogenerate migration command':=> alembic revision --autogenerate -m 'Initial migration' Then Finally, to apply the migration to the database: => alembic upgrade head ")
            input("Press Enter to start the FastAPI server...")
            print("Starting FastAPI server...")
            subprocess.run(["uvicorn", "main:app", "--reload"], cwd=project_name)
        except KeyboardInterrupt:
            print("\nServer stopped by user.")
            sys.exit(0)
        except subprocess.CalledProcessError:
         print("Error: Alembic failed to initialize.")
        sys.exit(1)
    else:
        print("Warning: main.py not found. Server not started.")

if __name__ == "__main__":
    main()
