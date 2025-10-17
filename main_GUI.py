from Wplace.find_last_png import find_last_one


template = 'template.png'

timeline_folder = 'timeline'
timeline = find_last_one(timeline_folder, '^(\\d{8})_(\\d{6})\\.png$')

timeline_cropped_folder = 'timeline_cropped_png'
timeline_cropped = find_last_one(timeline_cropped_folder, '^(\\d{8})_(\\d{6})\\.png$')

timeline_color_folder = 'timeline_color'
timeline_color_finish = find_last_one(timeline_color_folder, '^finish_all_(\\d{8})_(\\d{6})\\.png$')
timeline_color_mask = find_last_one(timeline_color_folder, '^mask_all_(\\d{8})_(\\d{6})\\.png$')
timeline_color_todo = find_last_one(timeline_color_folder, '^todo_all_(\\d{8})_(\\d{6})\\.png$')

class Png():
    def __init__(self):
        self.timeline_folder = 'timeline'
        self.timeline_cropped_folder = 'timeline_cropped_png'
        self.timeline_color_folder = 'timeline_color'
        self.template = 'template.png'
        self.timeline = find_last_one(self.timeline_folder, '^(\\d{8})_(\\d{6})\\.png$')
        self.timeline_cropped = find_last_one(self.timeline_cropped_folder, '^(\\d{8})_(\\d{6})\\.png$')
        self.timeline_color_finish = find_last_one(self.timeline_color_folder, '^finish_all_(\\d{8})_(\\d{6})\\.png$')
        self.timeline_color_mask = find_last_one(self.timeline_color_folder, '^mask_all_(\\d{8})_(\\d{6})\\.png$')
        self.timeline_color_todo = find_last_one(self.timeline_color_folder, '^todo_all_(\\d{8})_(\\d{6})\\.png$')




if __name__ == "__main__":
    png = Png()
    print(f"Latest file in timeline folder: {png.timeline}")
    print(f"Latest file in cropped folder: {png.timeline_cropped}")
    print(f"Latest finish_all file in color folder: {png.timeline_color_finish}")
    print(f"Latest mask_all file in color folder: {png.timeline_color_mask}")
    print(f"Latest todo_all file in color folder: {png.timeline_color_todo}")
