
from setuptools import setup, find_packages

setup(
    name="spokenpy",
    version="0.1.1",
    author="Arun",
    description="Voice-driven programming language for accessibility",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition",
        "pyttsx3",
        "pyaudio",
    ],
    entry_points={
        "console_scripts": [
            "spokenpy=spokenpy.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Interpreters",
    ],
    python_requires='>=3.7',
)
