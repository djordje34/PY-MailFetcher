import sys # Imports are automatically detected (normally) in the script to freeze
import os 
import cx_Freeze
base = None 
from cx_Freeze import setup, Executable

if sys.platform=='win32':
    base = "Win32GUI"
#icon='icona.png'

#executables = [cx_Freeze.Executable("olg.py"),icon]    

target = Executable(
    script="getmail.py",
    base="Win32GUI",
    #compress=False,
    #copyDependentFiles=True,
    #appendScriptToExe=True,
    #appendScriptToLibrary=False,
    icon="email.ico"
)

cx_Freeze.setup(
        name = "E-mail Academic Fetcher",
        options = {"build_exe":{"packages":["tkinter","imaplib","email","datetime","tkinter.font","email.header"],'include_files':["charmander.txt","pikachu.txt"]}},
        version="0.1",
        executables=[target]) 