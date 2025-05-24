# Manga Reader App

A Streamlit-based application for reading manga using the MangaDex API. Search for manga, select from similar titles, choose chapters, and view pages with a clean interface. Includes related GIFs from Tenor and a random famous song (English, Japanese, or Korean). Can be bundled as a Windows executable (.exe) for easy distribution.

## Features
- Search for manga by name and select from similar titles.
- Browse and select chapters from a dropdown.
- Read manga pages with Previous/Next navigation and a Next Chapter button.
- View related GIFs scraped from Tenor.
- Play random famous songs via YouTube embed.
- Displays a random Japanese greeting for a cultural touch.
- Data sourced from [MangaDex](https://mangadex.org).
- Windows executable (.exe) for users without Python.

## Prerequisites
- Python 3.8 or higher (for development or creating the .exe)
- pip for installing dependencies
- Windows 10 or later (for running the .exe)

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
   - For broader distribution, digitally sign the .exe with a certificate (requires tools like Microsoft Sign Tool).

## Running the Executable
- Double-click `MangaReader.exe` in the `dist/MangaReader/` folder.
- A browser window should open with the manga reader app.
- If the app doesn’t open, run from Command Prompt to view errors:
  ```bash
  cd dist\MangaReader
  MangaReader.exe
  ```

## Usage
1. In the sidebar, enter a manga name (e.g., "Naruto") and click "Search."
2. Select a manga from the dropdown of similar titles.
3. Choose a chapter from the chapter dropdown.
4. Use "Previous Page" and "Next Page" buttons to navigate pages.
5. Click "Next Chapter" (if available) to read the next chapter.
6. Expand sections for related GIFs and a random song.

## License
This project is licensed under the MIT License. See `LICENSE.txt` for details.

## Dependencies
Listed in `requirements.txt`:
- streamlit>=1.37.0
- requests>=2.31.0
- beautifulsoup4>=4.12.3
- pyinstaller>=5.13.0 (for creating .exe)

## Notes
- **MangaDex API**: Uses public API for manga data and images. Be aware of rate limits.
- **Legal**: MangaDex hosts official and fan-translated content, which may be subject to copyright. This app only uses public API data.
- **Executable Size**: The .exe folder may be large (~100-200 MB) due to bundled dependencies.
- **Windows Defender**: Unsigned .exe files may be flagged. Add an exception or sign the .exe for distribution.
- **Internet**: The app requires an internet connection for MangaDex API and Tenor GIFs.

## Troubleshooting
- **Streamlit Import Error**: Ensure you’re in a clean virtual environment and include `--hidden-import streamlit --hidden-import importlib_metadata` in the PyInstaller command.
- **App Fails to Start**: Run the .exe from Command Prompt to view errors. Check if all dependencies are installed correctly.
- **Slow Image Loading**: Ensure a stable internet connection, as images are fetched from MangaDex.

## Contributing
Submit issues or pull requests to improve the app.

## Acknowledgments
- Manga data and images provided by [MangaDex](https://mangadex.org).
- GIFs sourced from [Tenor](https://tenor.com).
- Songs embedded via [YouTube](https://youtube.com).