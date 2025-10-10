
import yaml
from pprint import pprint

from watchdog.events import FileSystemEventHandler


config_path = 'config.yaml'

# 计算坐标
def calculate_coordinates(top_left_block, block_range):
    x_start, y_start = top_left_block
    width, height = block_range
    return [(x, y) for y in range(y_start, y_start + height) for x in range(x_start, x_start + width)]

# 计算裁剪坐标
def calculate_crop_coordinates(base_coordinates, offset):
    x1, y1, x2, y2 = base_coordinates
    return (x1 + offset[0], y1 + offset[1], x2 + offset[2], y2 + offset[3])

def update_config(config):
    # 更新配置
    config['block_cords'] = calculate_coordinates(
        config['top_left_block'],
        config['block_range']
    )

    config['merge']['crop_coordinates_png'] = calculate_crop_coordinates(
        config['upper_left_pixel'] + config['lower_right_pixel'],
        [0, 0, 1, 1]
    )

    config['merge']['crop_coordinates_jpg'] = calculate_crop_coordinates(
        config['upper_left_pixel'] + config['lower_right_pixel'],
        [-1, -1, 2, 2]
    )
    return config


class ConfigHandler(FileSystemEventHandler):
    def __init__(self, config_path, reload_event):
        self.config_path = config_path
        self.config = self.load_config()
        self.reload_event = reload_event  # 保存 Event

    def load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            config = update_config(config)
            # pprint(config)
            return config

    def on_modified(self, event):
        if event.src_path.endswith(self.config_path):
            print("配置文件已更新，重新加载...")
            self.config = self.load_config()
            self.reload_event.set()  # 通知主循环重新加载

    @property
    def block_cords(self):
        """监控区块坐标列表"""
        return self.config.get('block_cords', [])
    @property
    def monitor(self):
        """监控区块配置"""
        return self.config.get('monitor', {})
    @property
    def merge(self):
        """图像处理配置"""
        return self.config.get('merge', {})
    @property
    def table(self):
        """表格处理配置"""
        return self.config.get('table', {})


    @property
    def merge_interval(self):
        """区块合并间隔"""
        return self.config.get('merge', {}).get('interval', 3600)
    @property
    def timeline_file(self):
        """时间线文件路径"""
        return self.config.get('merge', {}).get('timeline_file', '')


if __name__ == "__main__":
    cfg = ConfigHandler(config_path, None)
    pprint(cfg.config)