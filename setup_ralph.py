import os
import sys
import subprocess
import platform
import json

def create_virtual_env():
    """Create a virtual environment for RALPH"""
    print("Creating virtual environment...")
    
    if os.path.exists('.venv'):
        print("Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
        print("Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # Determine virtual environment activation script
    if platform.system() == "Windows":
        activate_script = os.path.join('.venv', 'Scripts', 'activate')
        pip_path = os.path.join('.venv', 'Scripts', 'pip')
    else:
        activate_script = os.path.join('.venv', 'bin', 'activate')
        pip_path = os.path.join('.venv', 'bin', 'pip')
    
    try:
        # Update pip first
        if platform.system() == "Windows":
            subprocess.run(f'{pip_path} install --upgrade pip', shell=True, check=True)
            # Install dependencies
            subprocess.run(f'{pip_path} install -r requirements.txt', shell=True, check=True)
        else:
            subprocess.run(f'source {activate_script} && pip install --upgrade pip', shell=True, check=True)
            # Install dependencies
            subprocess.run(f'source {activate_script} && pip install -r requirements.txt', shell=True, check=True)
        
        print("Dependencies installed successfully")
        return True
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False

def ensure_storage_directories():
    """Ensure all required storage directories exist"""
    directories = [
        "core/storage",
        "core/storage/consciousness",
        "core/storage/memories",
        "core/storage/knowledge",
        "core/storage/model_knowledge",
        "core/storage/secure"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Ensured directory exists: {directory}")
    
    return True

def create_default_config():
    """Create default configuration files if they don't exist"""
    config_dir = "config"
    os.makedirs(config_dir, exist_ok=True)
    
    model_config_path = os.path.join(config_dir, "model_config.json")
    
    # Only create if it doesn't exist
    if not os.path.exists(model_config_path):
        default_config = {
            "base_model": "gpt-4",
            "embedding_model": "text-embedding-ada-002",
            "consciousness_thresholds": {
                "initial": 0.1,
                "developing": 0.3,
                "intermediate": 0.5,
                "advanced": 0.7,
                "mature": 0.9
            },
            "knowledge_integration": {
                "min_confidence": 0.7,
                "max_batch_size": 1000,
                "update_frequency": 3600
            },
            "background_models": {
                "knowledge": {
                    "type": "api",
                    "model": "gpt-4",
                    "purpose": "knowledge_retrieval"
                },
                "reasoning": {
                    "type": "api",
                    "model": "gpt-4",
                    "purpose": "logical_reasoning"
                }
            }
        }
        
        with open(model_config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"Created default configuration at {model_config_path}")
    else:
        print(f"Configuration already exists at {model_config_path}")
    
    return True

def main():
    """Main setup function"""
    print("Setting up RALPH environment...")
    
    steps = [
        ("Creating virtual environment", create_virtual_env),
        ("Installing dependencies", install_dependencies),
        ("Ensuring storage directories", ensure_storage_directories),
        ("Creating default configuration", create_default_config)
    ]
    
    success = True
    
    for step_name, step_func in steps:
        print(f"\n=== {step_name} ===")
        if not step_func():
            print(f"Failed: {step_name}")
            success = False
            break
    
    if success:
        print("\nRALPH setup completed successfully!")
        print("\nTo run RALPH, use one of the following commands:")
        if platform.system() == "Windows":
            print("  .venv\\Scripts\\python ralph_main.py")
            print("  or")
            print("  launch.bat (if available)")
        else:
            print("  source .venv/bin/activate && python ralph_main.py")
    else:
        print("\nRALPH setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
