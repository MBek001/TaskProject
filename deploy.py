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

def create_virtual_environment(venv_path):
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment at {venv_path}...")
        venv.create(venv_path, with_pip=True)
    else:
        print(f"Virtual environment already exists at {venv_path}")

def activate_virtual_environment(venv_path):
    """Activate the virtual environment."""
    activate_script = os.path.join(venv_path, 'bin', 'activate_this.py')
    if os.path.exists(activate_script):
        with open(activate_script) as f:
            exec(f.read(), dict(__file__=activate_script))
    else:
        print(f"Could not find the activate script at {activate_script}")
        sys.exit(1)

def main():
    venv_path = "venv"  # Adjust this path as needed

    # Step 1: Create virtual environment if it doesn't exist
    create_virtual_environment(venv_path)

    # Step 2: Activate virtual environment
    activate_virtual_environment(venv_path)

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
