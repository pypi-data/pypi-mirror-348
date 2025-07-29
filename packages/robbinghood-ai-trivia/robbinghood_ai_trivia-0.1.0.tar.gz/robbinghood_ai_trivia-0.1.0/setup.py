from setuptools import setup, find_packages

setup(
    name="robbinghood-ai-trivia",
    version="0.1.0",
    packages=find_packages(include=["ai", "ai.*", "camera", "camera.*", "core", "core.*", "ocr", "ocr.*", "ui", "ui.*"]),
    py_modules=["main", "config"],  # Include main.py and config.py as standalone modules
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "robbinhood-cam=main:main",
        ],
    },
)

