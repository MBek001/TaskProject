import os
import subprocess
import sys
import venv

def run_command(command, exit_on_fail=True):
    """Run a shell command and ensure it succeeds."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}: {command}")
        if exit_on_fail:
            sys.exit(result.returncode)
    return result.returncode



def create_virtual_environment(venv_path):
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment at {venv_path}...")
        venv.create(venv_path, with_pip=True)
    else:
        print(f"Virtual environment already exists at {venv_path}")

def activate_virtual_environment(venv_path):
    """Activate the virtual environment."""
    activate_script = os.path.join(venv_path, 'bin', 'activate')
    if os.path.exists(activate_script):
        command = f"source {activate_script}"
        print(f"Activating virtual environment: {command}")
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
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