
from pathlib import Path
from Wplace.find_last_png import find_last_one

base_folder = '模板'

main_exe = (Path(base_folder) / 'Wplace-GUI.exe').resolve()
image_process_exe = (Path(base_folder) / 'image_process.exe').resolve()
config_GUI_exe = (Path(base_folder) / 'config_GUI.exe').resolve()

template = (Path(base_folder) / 'template.png').resolve()

timeline_folder = (Path(base_folder) / 'timeline').resolve()
timeline = find_last_one(timeline_folder, r'^(\d{8})_(\d{6})\.png$')

timeline_cropped_folder = (Path(base_folder) / 'timeline_cropped_png').resolve()
timeline_cropped = find_last_one(timeline_cropped_folder, r'^(\d{8})_(\d{6})\.png$')

timeline_color_folder = (Path(base_folder) / 'timeline_color').resolve()
timeline_color_finish = find_last_one(timeline_color_folder, r'^finish_all_(\d{8})_(\d{6})\.png$')
timeline_color_mask = find_last_one(timeline_color_folder, r'^mask_all_(\d{8})_(\d{6})\.png$')
timeline_color_todo = find_last_one(timeline_color_folder, r'^todo_all_(\d{8})_(\d{6})\.png$')




if __name__ == "__main__":
    print(f"Main EXE: {main_exe}")
    print(f"Image Process EXE: {image_process_exe}")
    print(f"Config GUI EXE: {config_GUI_exe}")
    print(f"Template: {template}")
    print(f"Latest file in timeline folder: {timeline}")
    print(f"Latest file in cropped folder: {timeline_cropped}")
    print(f"Latest finish_all file in color folder: {timeline_color_finish}")
    print(f"Latest mask_all file in color folder: {timeline_color_mask}")
    print(f"Latest todo_all file in color folder: {timeline_color_todo}")
