import sys
from cx_Freeze import setup, Executable
from cx_Freeze.dist import build_exe

# Dependencies are automatically detected, but it might need fine tuning.
build_msi_options = {"add_to_path":True,"all_users":True,"install_icon":"D:\\Git\\Music-Player\\img\\tkicon.ico"}
build_exe_option={"include_files":[('D:\Git\Music-Player\img',"img" )]}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Music-Player",
        version = "1.0",
        description = "My GUI application!",
        options = {"bdist_msi": build_msi_options,"build_exe":build_exe_option},
        executables = [Executable("music_player.py", base=base,icon="D:\\Git\\Music-Player\\img\\tkicon.ico")])