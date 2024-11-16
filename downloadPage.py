import subprocess

import flet as ft

from common import default_download_path, snack_bar, aria2c_path, down_proc_list


def downTab(page: ft.Page):
    cols = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    t = ft.Tab(tab_content=ft.Row([
        ft.Text("下载")
    ]),
        content=ft.Container(
            cols,
            padding=8,
            expand=True,
        ),
    )
    # 用来存储进程对象
    download_proc = None
    trackers_list = ""

    bit_path = ft.TextField(autofocus=True, expand=True, multiline=True)
    download_path = ft.TextField(expand=True)
    trackers = ft.TextField(expand=True, multiline=True)
    download_path.disabled = True
    download_path.value = default_download_path[0]

    def on_dialog_result(e: ft.FilePickerResultEvent):
        download_path.value = e.path
        page.client_storage.set("download_path", e.path)
        download_path.update()

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()

    download_log = ft.Text()

    def download(e):
        if bit_path.value == "":
            snack_bar.content = ft.Text("请输入磁力链接")
            snack_bar.open = True
            page.update()
            return
        if download_path.value == "":
            snack_bar.content = ft.Text("请选择下载路径")
            snack_bar.open = True
            page.update()
            return

        global trackers_list
        start_download_button.disabled = True
        stop_download_button.disabled = False
        page.update()
        trackers_list = ",".join(trackers.value.split())

        print(aria2c_path, "--dir=" + download_path.value, "--bt-tracker=" + trackers_list,

              bit_path.value)

        global download_proc
        # 启动子进程并实时捕获输出
        download_proc = subprocess.Popen(
            [aria2c_path, "--dir=" + download_path.value, "--bt-tracker=" + trackers_list,
             bit_path.value],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        down_proc_list.append(download_proc)

        # 实时读取标准输出
        for line in download_proc.stdout:
            if line.strip() != "":
                download_log.value = line
                download_log.update()

        # 等待程序结束
        download_proc.wait()

    def stop_download(e):
        start_download_button.disabled = False
        stop_download_button.disabled = True
        start_download_button.text = "继续下载"
        page.update()

        global download_proc
        if download_proc:
            download_proc.terminate()  # 或者使用 download_proc.kill()
            download_proc = None

    start_download_button = ft.ElevatedButton("开始下载", on_click=download)
    stop_download_button = ft.ElevatedButton("停止下载", on_click=stop_download, color=ft.colors.RED_500,
                                             disabled=True)

    cols.controls.append(
        ft.Column([
            ft.Row(
                [
                    ft.Text("磁力链接地址"),
                    bit_path
                ]),
            ft.Row(
                [
                    ft.Text("下载路径"),
                    ft.Container(
                        download_path,
                        on_click= lambda e: file_picker.get_directory_path("选择下载路径")
                    )
                ]
            ),
            ft.Row([
                ft.Text("Trackers"),
                trackers
            ]),
            ft.Row([
                start_download_button,
                stop_download_button
            ]),
            download_log
        ]))
    page.update()
    return t
