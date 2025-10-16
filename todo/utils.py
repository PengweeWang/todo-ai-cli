import datetime
import os
import platform
import subprocess
from importlib.resources import files


STORAGE_FILE = os.path.join(os.path.expanduser('~'), '.local', 'share', 'td', 'todo.json')
ARCHIVE_FILE = os.path.join(os.path.expanduser('~'), '.local', 'share', 'td', 'archive.json')
CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.local', 'share', 'td', 'config.ini')

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def create_todo_item(title, 
                     description = "",
                     status = "",
                     create_time = current_time,
                     deadline = "",
                     complete_time = "",
                     tags = "",
                     location = ""):
    return {
        "Title": title,
        "Description": description,
        "Status": status,
        "CreateTime": create_time,
        "Deadline": deadline,  
        "CompleteTime": complete_time,
        "Tags": tags,
        "Location": location
    }

def check_storage():
    user_home = os.path.expanduser('~')
    
    td_dir = os.path.join(user_home, '.local', 'share', 'td')
    archive_dir = os.path.join(td_dir, 'archive.json')
    config_file = os.path.join(td_dir, 'config.ini')
    todo_file = os.path.join(td_dir, 'todo.json')
    # 创建主目录
    os.makedirs(td_dir, exist_ok=True)
    
    
    # 创建配置文件
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            pass  # 创建空文件
    
    # 创建todo.json文件
    if not os.path.exists(todo_file):
        with open(todo_file, 'w') as f:
            pass  # 创建空文件
    
    # 创建archive.json文件
    if not os.path.exists(archive_dir):
        with open(archive_dir, 'w') as f:
            pass  # 创建空文件
    
    
from datetime import datetime

def process_time(natural_time: str) -> str:
    # 分割月日部分和时分部分
    month_day_part, hour_minute_part = natural_time.split('-')
    
    def format_month_day(part: str) -> tuple:
        # 统一月日分隔符为.，然后分割为月和日
        part = part.replace(':', '.').replace('：', '.')
        month, day = part.split('.')
        # 补零确保月和日为两位数字
        return month.zfill(2), day.zfill(2)
    
    def format_hour_minute(part: str) -> tuple:
        # 统一时分分隔符为:，然后分割为时和分
        part = part.replace('.', ':').replace('：', ':')
        hour, minute = part.split(':')
        # 补零确保时和分为两位数字
        return hour.zfill(2), minute.zfill(2)
    
    # 处理月日和时分
    month, day = format_month_day(month_day_part)
    hour, minute = format_hour_minute(hour_minute_part)
    
    # 获取当前年份
    current_year = datetime.now().strftime("%Y")
    
    # 拼接为最终格式
    return f"{current_year}-{month}-{day} {hour}:{minute}"
    
    
def open_help_document():
    try:
        help_file = files("todo").joinpath("help.html")
        help_file_path = str(help_file.resolve())  # 转为绝对路径

        # Windows用start，macOS用open，Linux用xdg-open
        if platform.system() == "Windows":
            subprocess.run(["start", help_file_path], shell=True, check=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", help_file_path], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", help_file_path], check=True)
    
    except Exception as e:
        print(f"帮助文档详见：{help_file_path}")    
    

if __name__ == "__main__":
    print(process_time("10.20-14:30"))
    print(process_time("1.5-9：5"))
    
    
    
    
    
    
    