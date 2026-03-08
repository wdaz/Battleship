# Battleship Game

## Building the Executable

To build the standalone `.exe` file for the game, make sure you have `pyinstaller` installed and run the following command from the root folder of the project:

```bash
python -m PyInstaller --noconfirm --onedir --windowed --paths src --add-data "assets;assets" src/main.py
```

After the build completes successfully, you will find `main.exe` inside the `dist/main/` folder.
