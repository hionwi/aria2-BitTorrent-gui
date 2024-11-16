import flet as ft

from common import down_proc_list, snack_bar, default_download_path
from downloadPage import downTab


def main(page: ft.Page):
    def window_event(e):
        if e.data == "close":
            for proc in down_proc_list:
                if proc:
                    proc.terminate()
            page.window.destroy()

    page.window.prevent_close = True
    page.window.on_event = window_event

    page.overlay.append(snack_bar)

    if page.client_storage.contains_key("download_path"):
        default_download_path[0] = page.client_storage.get("download_path")

    page.fonts = {
        "NotoSansSC": "fonts/NotoSansSC-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="NotoSansSC")
    page.title = "Aria2c GUI"
    new_button = ft.ElevatedButton(
        text="新建下载",
    )
    tabs = ft.Tabs(
        animation_duration=300,
        tabs=[downTab(page),ft.Tab(tab_content=new_button)],
        expand=True,
    )


    def new_download(e):
        tabs.tabs.pop()
        tabs.tabs.append(downTab(page))
        tabs.tabs.append(ft.Tab(tab_content=new_button))
        tabs.selected_index = len(tabs.tabs) - 2
        page.update()

    new_button.on_click = new_download

    page.add(tabs)


ft.app(main)
