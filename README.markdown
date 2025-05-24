# Manga Reader App

A Streamlit-based application for reading manga using the MangaDex API. Search for manga, select from similar titles, choose chapters, and view pages with a clean interface. Includes related GIFs from Tenor and more. Can be bundled as a Windows executable (.exe) for easy distribution.

## Prerequisites
- Python 3.8 or higher
- pip for installing dependencies
- Windows 10 or later

## Installation
1. **Clone or download the repository**:
   ```bash
   git clone <repository-url>
   cd manga_reader
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app locally** (optional, for testing):
   ```bash
   streamlit run manga_reader.py
   ```
   - Open the provided URL (e.g., `http://localhost:8501`) in your browser.

## Creating the Windows Executable (.exe)
To create a standalone .exe for Windows users:

1. **Create a clean virtual environment** (to avoid dependency conflicts):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies in the virtual environment**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run PyInstaller with hidden imports**:
   ```bash
   pyinstaller --onedir --noconsole --name MangaReader --add-data "manga_reader.py;." --hidden-import streamlit --hidden-import importlib_metadata run.py
   ```
   - `--onedir`: Creates a directory with all files (faster startup).
   - `--noconsole`: Hides the terminal window.
   - `--name MangaReader`: Names the executable `MangaReader.exe`.
   - `--add-data "manga_reader.py;."`: Includes the main script.
   - `--hidden-import streamlit --hidden-import importlib_metadata`: Ensures Streamlit and its metadata are included.
   - This creates a `dist/MangaReader/` folder with the executable and dependencies.

4. **Locate the executable**:
   - Find `MangaReader.exe` in `dist/MangaReader/`.
   - Copy the entire `dist/MangaReader/` folder to distribute.

5. **Handle Windows Defender** (if needed):
   - If Windows Defender flags the .exe, add an exception:
     - Go to Windows Security > Virus & Threat Protection > Manage Settings > Add or Remove Exclusions.
     - Add the `MangaReader.exe` file or folder.
   - For broader distribution, digitally sign the .exe with a certificate.

## Usage
1. In the sidebar, enter a manga name (e.g., "Naruto") and click "Search."
2. Select a manga from the dropdown of similar titles.
3. Choose a chapter from the chapter dropdown.
Enjoy reading~

## License
This project is licensed under the MIT License. See `LICENSE.txt` for details.

