from setuptools import setup, find_packages

setup(
    name="nuggetry",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "pygetwindow",
        "pyttsx3",
        "requests",
        "pillow",
        "pyobjc-core; platform_system=='Darwin'",
        "pyobjc; platform_system=='Darwin'",
        "pywin32; platform_system=='Windows'"
    ],
    entry_points={
        "console_scripts": [
            "nuggetry = nuggetry.__main__:main"
        ]
    },
    author="Your Name",
    description="Nuggetry: a Lua-like scripting language in Python for automation",
    long_description="Nuggetry is a scripting language that lets you automate your PC, speak, get websites, and more.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
