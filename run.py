import subprocess
import sys
import os

def main():
    # Set working directory to script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Command to run Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", "manga_reader.py",
        "--server.port=8501", "--global.developmentMode=false"
    ]
    
    # Run Streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()