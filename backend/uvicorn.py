import sys
from pathlib import Path

# Configure the environment and add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

# Configure Uvicorn
from uvicorn import Config

def main():
    app = import_module(__name__)
    config = Config(app, host="0.0.0.0", port=8000, log_level="debug")
    config.run()

if __name__ == "__main__":
    main()