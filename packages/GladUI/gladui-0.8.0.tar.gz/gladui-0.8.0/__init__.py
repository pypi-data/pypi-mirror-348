import os
import platform
from pathlib import Path

# Load correct DLLs only on Windows
if platform.system() == "Windows":
    dll_dir = Path(__file__).resolve().parent / "lib" / "windows"
    os.add_dll_directory(str(dll_dir))

# Import the compiled C++ module
import GladUI
