from setuptools import setup, Extension
import platform
import os

# Determine the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Read the contents of README.md
with open("README.md", encoding='utf-8') as f:
    long_description = f.read()

# Platform-specific configurations
system = platform.system()
extra_compile_args = ["-std=c++17"]
include_dirs = ["include", "assets/GladG"]
libraries = []
library_dirs = []
extra_link_args = []

if system == "Windows":
    libraries = ["SDL2", "SDL2_ttf", "SDL2_image", "SDL2_mixer"]
    library_dirs = ["lib/windows"]
elif system == "Darwin":  # macOS
    libraries = ["SDL2", "SDL2_ttf", "SDL2_image", "SDL2_mixer"]
    extra_compile_args.append("-stdlib=libc++")  # Clang on macOS
elif system == "Linux":
    libraries = ["SDL2", "SDL2_ttf", "SDL2_image", "SDL2_mixer"]
    # Assumes SDL2 is installed globally

# Define the extension module
GladUI_ext = Extension(
    "GladUI", 
    sources=["GladUI.cpp"],
    include_dirs=include_dirs,
    libraries=libraries,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c++"
)

# Setup configuration
setup(
    name="GladUI",
    version="0.8.0",
    description="Cross-platform C++ GUI engine using SDL2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Navthej",
    packages=["."],
    package_data={
        "GladUI": [
            "lib/windows/*.dll",
            "include/SDL2/*.h",
            "assets/GladG/*.h",
        ]
    },
    include_package_data=True,
    ext_modules=[GladUI_ext],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
