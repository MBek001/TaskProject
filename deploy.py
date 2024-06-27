import os
import sys
import subprocess

def run_command(command):
    """Run a shell command and ensure it succeeds."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}: {command}")
        sys.exit(result.returncode)

def main():
    # Step 1: Generate Alembic migrations
    print("Generating Alembic migrations...")
    run_command("alembic revision --autogenerate -m 'create users table'")

    # Step 2: Apply Alembic migrations
    print("Applying Alembic migrations...")
    run_command("alembic upgrade head")

    # Step 3: Start Uvicorn server
    print("Starting Uvicorn server...")
    run_command("uvicorn main:app --host 0.0.0.0 --port 10000")

if __name__ == "__main__":
    main()
