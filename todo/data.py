import json
import os
from configparser import ConfigParser

class TodoDataManager:
    def __init__(self, file_path: str, archive_path: str = None):
        self.file_path = file_path
        self.archive_path = archive_path
        self.data = self.__load_todos()
    

    def __load_todos(self):
        """从JSON文件加载待办事项"""
        if not os.path.exists(self.file_path):
            print(f"文件 {self.file_path} 不存在")
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                if os.path.getsize(self.file_path) == 0:
                    return []
                todos = json.load(f)
                return todos
        except Exception as e:
            print(f"读取文件时出错: {e}")
            return []
        
    def save_todos(self):
        """将待办事项保存到JSON文件"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存文件时出错: {e}")
            
    def add_todo(self, todo_item: dict):
        """添加新的待办事项"""
        self.data.append(todo_item)
        self.save_todos()
    
    def set_todo(self, index: int, updated_item: dict):
        """修改指定索引的待办事项"""
        if 0 <= index < len(self.data):
            self.data[index] = updated_item
            self.save_todos()
        else:
            print(f"索引 {index} 超出范围")
            
    def get_todo(self, index: int):
        """获取指定索引的待办事项"""
        if 0 <= index < len(self.data):
            return self.data[index]
        else:
            print(f"索引 {index} 超出范围")
            return None
    
    def get_all_todos(self):
        """获取所有待办事项"""
        return self.data
    
    def remove_todo(self, index: int):
        """删除指定索引的待办事项"""
        if 0 <= index < len(self.data):
            removed_item = self.data.pop(index)
            self.save_todos()
            return removed_item
        else:
            print(f"索引 {index} 超出范围")
            return None
    
    def archive_todo(self):
        """归档已完成事项到指定文件"""
        archived_items = [item for item in self.data if item.get("Status") == "已完成"]
        if not archived_items:
            print("没有已完成的事项可归档")
            return
        
        # 保存归档文件
        try:
            with open(self.archive_path, 'a', encoding='utf-8') as f:
                for item in archived_items:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"归档文件时出错: {e}")
            return
        
        # 从当前待办中移除已归档事项
        self.data = [item for item in self.data if item.get("Status") != "已完成"]
        self.save_todos()
        print(f"已归档 {len(archived_items)} 项待办事项到 {self.archive_path}")
    
    def get_archived_todos(self):
        """获取所有归档的待办事项"""
        if not self.archive_path or not os.path.exists(self.archive_path):
            print(f"归档文件 {self.archive_path} 不存在")
            return []
        try:
            with open(self.archive_path, 'r', encoding='utf-8') as f:
                archived_items = [json.loads(line) for line in f if line.strip()]
                return archived_items
        except Exception as e:
            print(f"读取归档文件时出错: {e}")
            return []
        

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.__load_config()
        self.api_key = self.get_config('default', 'api_key')
        self.base_url = self.get_config('default', 'base_url')
        self.model_id = self.get_config('default', 'model_id')
    
    def __load_config(self):
        """加载配置文件"""
        config = ConfigParser()
        if os.path.exists(self.config_path):
            config.read(self.config_path, encoding='utf-8')
        return config
    
    def get_config(self, option: str, section: str = "default"):
        """获取指定配置项"""
        if self.config.has_section(section):
            return self.config.get(section, option, fallback=None)
        return None

    def set_config(self, option: str, value: str, section: str = "default"):
        """设置指定配置项"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)
