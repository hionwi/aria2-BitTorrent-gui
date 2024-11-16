import os
import sys
import flet as ft

down_proc_list = []
default_download_path = [""]

if getattr(sys, 'frozen', False):
    # 如果程序被打包，使用 PyInstaller 提供的路径
    base_path = sys._MEIPASS
else:
    # 否则使用当前工作目录
    base_path = os.path.abspath(".")

aria2c_path = os.path.join(base_path, "assets", "aria2c.exe")
snack_bar = ft.SnackBar(
    content=ft.Text("Hello, world!"),
)