import sys
import subprocess
import platform
import os

def create_venv():
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

def activate_venv():
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "activate")
    else:
        return os.path.join("venv", "bin", "activate")

def install_requirements():
    print("Installing requirements...")
    python_cmd = os.path.join("venv", "Scripts", "python") if platform.system() == "Windows" else os.path.join("venv", "bin", "python")
    pip_cmd = os.path.join("venv", "Scripts", "pip") if platform.system() == "Windows" else os.path.join("venv", "bin", "pip")
    
    subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
    
    # Install development dependencies
    subprocess.run([pip_cmd, "install", "black", "flake8", "isort"], check=True)

def setup_database():
    print("Setting up database...")
    flask_cmd = os.path.join("venv", "Scripts", "flask") if platform.system() == "Windows" else os.path.join("venv", "bin", "flask")
    
    # Set Flask app environment variable
    os.environ["FLASK_APP"] = "app.py"
    
    # Run migrations
    subprocess.run([flask_cmd, "db", "upgrade"], check=True)

def main():
    try:
        create_venv()
        venv_activate = activate_venv()
        
        print(f"\nSetup completed successfully!")
        print(f"\nTo activate the virtual environment:")
        if platform.system() == "Windows":
            print(f"    venv\\Scripts\\activate")
        else:
            print(f"    source venv/bin/activate")
            
        print("\nTo start the development server:")
        if platform.system() == "Windows":
            print(f"    venv\\Scripts\\python app.py")
        else:
            print(f"    venv/bin/python app.py")
        
        print("\nInstalling dependencies...")
        install_requirements()
        
    except Exception as e:
        print(f"Error during setup: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 