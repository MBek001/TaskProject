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

    # Step 4: Generate Alembic migrations
    print("Generating Alembic migrations...")
    alembic_revision_code = run_command("alembic revision --autogenerate -m 'create6363'", exit_on_fail=False)

    if alembic_revision_code != 0:
        print("Alembic revision generation failed. Checking for existing migrations.")
        print("Clearing old Alembic migrations...")
        # Reset Alembic by clearing migration files and the version table (use with caution)
        migrations_path = os.path.join(os.getcwd(), 'migrations', 'versions')
        for file in os.listdir(migrations_path):
            os.remove(os.path.join(migrations_path, file))
        run_command("alembic downgrade base")
        run_command("alembic stamp head")

        print("Generating Alembic migrations again...")
        run_command("alembic revision --autogenerate -m 'create6363'")

    # Step 5: Apply Alembic migrations
    print("Applying Alembic migrations...")
    run_command("alembic upgrade head")

    # Step 6: Start Uvicorn server
    print("Starting Uvicorn server...")
    run_command("uvicorn main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()
