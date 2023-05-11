from cx_Freeze import setup, Executable

direct = "c:\\Users\\user\\Desktop\\assistant\\venv\\Lib\\site-packages\\pyttsx3"  # path to the pyttsx3

build_exe_options = {
    "includes": [
        "textHandler",
        "audioProcessor",
        "pvporcupine",
        "pvrecorder",
        "speech_recognition",
        "pyttsx3",
        "traceback",
        "datetime",
        "re",
        "requests",
        "googletrans",
        "pyautogui",
        "keyboard",
        "webbrowser",
        "user",
        "time",
        "ctypes",
        "comtypes",
        "pycaw",
        "pybrightness",
        "fuzzywuzzy",
        "pydub",
        "torch",
        "Levenshtein",
        "PyQt5"
    ],
    "packages": ["os", "sys"],
    "include_files": [
        (direct, "lib/pyttsx3"),
        "data",
        "commands.json"
    ]
}

setup(
    name="Quant",
    version="0.5",
    description="Voice assistant for programmers",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", target_name="assistant")],
)
