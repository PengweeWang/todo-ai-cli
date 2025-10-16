from datetime import datetime
from typing import List, Dict
from colorama import init, Fore, Back, Style

# 初始化colorama
init(autoreset=True)

class TodoRenderer:
    def __init__(self, data):
        self.todos = data


    def get_status_emoji(self, status: str, deadline: str, complete_time: str) -> tuple:
        """根据状态返回对应的emoji和颜色"""
        if complete_time and complete_time != "null":
            return "✅", Fore.GREEN  # 已完成
        
        current_time = datetime.now()
        deadline_time = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        
        if status == "待处理":
            if current_time > deadline_time:
                return "❌", Fore.RED  # 已超时未完成
            else:
                return "⏩", Fore.BLUE  # 进行中
        elif status == "已完成":
            return "✅", Fore.GREEN
        else:
            return "⏩", Fore.BLUE  # 默认进行中
    
    def categorize_todos(self) -> Dict[str, List[Dict]]:
        """将待办事项分类，同时记录原始索引"""
        categories = {
            "ToDo": [],    # 进行中的事项
            "Finished": [], # 已完成的事项
            "Unfinished": [] # 未完成的事项（已超时）
        }
        
        # 遍历所有待办事项，记录原始索引（i为原始列表中的索引）
        for i, todo in enumerate(self.todos):
            emoji, color = self.get_status_emoji(
                todo.get("Status", ""),
                todo.get("Deadline", ""),
                todo.get("CompleteTime", "")
            )
            
            todo_with_emoji = todo.copy()
            todo_with_emoji["emoji"] = emoji
            todo_with_emoji["color"] = color
            todo_with_emoji["original_index"] = i  # 保存原始索引
            
            if emoji == "✅":
                categories["Finished"].append(todo_with_emoji)
            elif emoji == "❌":
                categories["Unfinished"].append(todo_with_emoji)
            else:  # ⏩
                categories["ToDo"].append(todo_with_emoji)
        
        return categories
    
    def format_time(self, time_str: str) -> str:
        """格式化时间显示"""
        if not time_str or time_str == "null":
            return "未设置"
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            return dt.strftime("%m-%d %H:%M")
        except:
            return time_str
    
    def render_todo_item(self, todo: Dict) -> str:
        """渲染单个待办事项"""
        emoji = todo.get("emoji", "⏩")
        color = todo.get("color", Fore.WHITE)
        title = todo.get("Title", "无标题")
        tags = todo.get("Tags", "")
        location = todo.get("Location", "")
        deadline = self.format_time(todo.get("Deadline", ""))
        
        # 构建带颜色的输出字符串
        parts = [f"{color}{emoji} {Style.BRIGHT}{Fore.WHITE}{title}{Style.RESET_ALL}"]
        
        if tags:
            parts.append(f"{Fore.YELLOW}@{tags}{Style.RESET_ALL}")
            
        parts.append(f"{Fore.CYAN}@end: {deadline}{Style.RESET_ALL}")
        
        if location:
            parts.append(f"{Fore.MAGENTA}📍 {location}{Style.RESET_ALL}")
        
        return f"{color}" + " ".join(parts)
    
    def render_section_header(self, title: str, emoji: str, color):
        """渲染分区标题"""
        print(f"{Style.BRIGHT}{color}{emoji} {title}")
    
    def render(self, category: str = "all"):
        """渲染所有待办事项，显示原始索引+1作为序号"""
        categories = self.categorize_todos()
        
        print()
        
        # 渲染 ToDo 部分
        if categories["ToDo"]:
            self.render_section_header("ToDo", "📝", Fore.BLUE)
            for todo in categories["ToDo"]:
                # 使用原始索引+1作为序号
                original_num = todo["original_index"] + 1
                print(f"  {Fore.WHITE}{original_num:2d}.{Style.RESET_ALL} {self.render_todo_item(todo)}")
            print()  # 空行
        else:
            if category == "all":
                print(f"  {Fore.GREEN}🎉 暂无进行中的任务{Style.RESET_ALL}")
                print()  # 空行
        
        # 渲染 Finished 部分
        if categories["Finished"]:
            self.render_section_header("Finished", "✅", Fore.GREEN)
            for todo in categories["Finished"]:
                original_num = todo["original_index"] + 1
                print(f"  {Fore.WHITE}{original_num:2d}.{Style.RESET_ALL} {self.render_todo_item(todo)}")
            print()  # 空行
        # else:
        #     print(f"  {Fore.CYAN}📝 暂无已完成的任务{Style.RESET_ALL}")
        #     print()  # 空行
        
        # 渲染 Unfinished 部分
        if categories["Unfinished"]:
            self.render_section_header("Unfinished", "❌", Fore.RED)
            for todo in categories["Unfinished"]:
                original_num = todo["original_index"] + 1
                print(f"  {Fore.WHITE}{original_num:2d}.{Style.RESET_ALL} {self.render_todo_item(todo)}")
            print()  # 空行
        # else:
        #     print(f"  {Fore.YELLOW}👍 暂无未完成的任务{Style.RESET_ALL}")
        #     print()  # 空行

def render_todo_item(todo: Dict) -> str:
    # 渲染任务信息

    print(Fore.CYAN + Style.BRIGHT + "📋 任务详情")


    # 标题
    print(f"📝 {Fore.GREEN}标题：{Fore.WHITE}{todo['Title']}")

    # 描述
    print(f"📝 {Fore.GREEN}描述：{Fore.WHITE}{todo['Description']}")

    # 状态（颜色区分）
    status_color = Fore.GREEN if todo['Status'] == "已完成" else Fore.YELLOW
    print(f"⏳ {Fore.GREEN}状态：{status_color}{todo['Status']}")

    # 创建时间
    print(f"🕒 {Fore.GREEN}创建时间：{Fore.BLUE}{todo['CreateTime']}")

    # 截止日期（无时间则灰色）
    deadline_color = Fore.RED if todo['Deadline'] != "null" else Fore.LIGHTBLACK_EX
    print(f"⏰ {Fore.GREEN}截止日期：{deadline_color}{todo['Deadline']}")

    # 完成时间
    complete_text = todo['CompleteTime'] if todo['CompleteTime'] != "null" else "未完成"
    complete_color = Fore.GREEN if todo['CompleteTime'] != "null" else Fore.LIGHTBLACK_EX
    print(f"✅ {Fore.GREEN}完成时间：{complete_color}{complete_text}")

    # 标签
    print(f"🏷️ {Fore.GREEN}标签：{todo['Tags']}")

    # 地点
    loc_text = todo['Location'] if todo['Location'] != "null" else "未指定"
    loc_color = Fore.CYAN if todo['Location'] != "null" else Fore.LIGHTBLACK_EX
    print(f"📍 {Fore.GREEN}地点：{loc_color}{loc_text}")



# 主程序
if __name__ == "__main__":
    # from data import TodoDataManager
    # from utils import STORAGE_FILE, ARCHIVE_FILE
    # data_manager = TodoDataManager(STORAGE_FILE, ARCHIVE_FILE)
    # renderer = TodoRenderer(data_manager.get_all_todos())
    # renderer.render()
    task = {
        "Title": "完成数学作业",
        "Description": "完成数学作业",
        "Status": "待处理",
        "CreateTime": "2025-10-16 22:00",
        "Deadline": "2025-10-17 22:00", 
        "CompleteTime": "null",
        "Tags": "学习",
        "Location": "图书馆"
    }
    
    render_todo_item(task)