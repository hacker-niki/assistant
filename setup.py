from cx_Freeze import setup, Executable

direct = "c:\\Users\\user\\Desktop\\assistant\\venv\\Lib\\site-packages\\pyttsx3"  # path to the pyttsx3

build_exe_options = {
    "includes": [
        "textHandler",
        "audioProcessor",
        "functions",
        "assistant",
        "app",
        "FirstWindow",
        "user",
        "ui",
        "json",
        "sys",
        "pvporcupine",
        "pvrecorder",
        "multiprocessing",
        "os",
        "traceback",
        "pyttsx3",
        "speech_recognition",
        "torch",
        "googletrans",
        "pydub",
        "tkinter",
        "pathlib",
        "sounddevice",
        "tkPDFViewer2",
        "datetime",
        "random",
        "re",
        "subprocess",
        "time",
        "webbrowser",
        "ctypes",
        "keyboard",
        "pyautogui",
        "pybrightness",
        "requests",
        "comtypes",
        "fuzzywuzzy",
        "num_to_rus",
        "pycaw",
        "PyQt5",
        "multiprocessing"
    ],
    "packages": ["os", "sys"],
    "include_files": [
        (direct, "lib/pyttsx3"),
        "data",
        "commands.json",
        "uiData",
        "data.json"
    ]
}
GUI = Executable(
    script="ui.py",
    base='Win32GUI',
    target_name="assistant"
)

setup(
    name="Quant",
    version="0.9.5",
    description="Voice assistant for programmers",
    options={"build_exe": build_exe_options},
    executables=[GUI]
)
