import os
import subprocess
import sys
import venv

def run_command(command):
    """Run a shell command and ensure it succeeds."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}: {command}")
        sys.exit(result.returncode)

def main():
    venv_path = "venv"  # Adjust this path as needed

    # Step 1: Create virtual environment if it doesn't exist
    run_command(" virtualenv .venv")

    # Step 2: Activate virtual environment
    run_command("source .venv/bin/activate")

    # Step 3: Install requirements from requirements.txt
    print("Installing requirements from requirements.txt...")
    run_command("pip install -r requirements.txt")

    # Step 4: Generate Alembic migrations
    print("Generating Alembic migrations...")
    run_command("alembic revision --autogenerate -m 'creating db'")

    # Step 5: Apply Alembic migrations
    print("Applying Alembic migrations...")
    run_command("alembic upgrade head")

    # Step 6: Start Uvicorn server
    print("Starting Uvicorn server...")
    run_command("uvicorn main:app --host 0.0.0.0 --port 10000")

if __name__ == "__main__":
    main()
