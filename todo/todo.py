import argparse
from .utils import check_storage, create_todo_item, process_time
from .render import TodoRenderer as Renderer
from .render import render_todo_item
from .utils import STORAGE_FILE, ARCHIVE_FILE, open_help_document
from .data import TodoDataManager
from .agent import todo_agent
from .agent import config


data_manager = TodoDataManager(STORAGE_FILE, ARCHIVE_FILE)




def build_parser():
    parser = argparse.ArgumentParser(prog="todo", description="待办记事cli.")
    subparser = parser.add_subparsers(dest="command", help="add/print/set/archive/config/help")
    add_parser = subparser.add_parser("add", help="添加待办事项")
    print_parser = subparser.add_parser("print", help="查看待办事项")
    set_parser = subparser.add_parser("set", help="对一项待办的具体内容进行修改")
    archive_parser = subparser.add_parser("archive", help="对代办事项进行归档及归档查看")
    config_parser = subparser.add_parser("config", help="设置todo的api-key，归档周期等")
    help_parser = subparser.add_parser("help", help="查看帮助文档")
    
    # 添加待办
    add_parser.add_argument('title', help="待办事件的内容")
    add_parser.add_argument('-a', '--auto', help="使用LLM自动提取并构建待办事件", action="store_true")
    add_parser.add_argument('-d', '--deadline', help="指定事件的截止时间", type=str)
    add_parser.add_argument('-t', '--tags', help="设置事件所属的tag",type=str)
    add_parser.add_argument('-des', '--description', help="对事件添加附加信息", type=str)
    
    # 查看待办
    print_parser.add_argument("id", help="查看特定事项的序号，留空则打印所有", default=None, nargs='?')
    
    # 修改待办
    set_parser.add_argument('id', help="需要修改待办事项的需要")
    set_parser.add_argument("-f", "--finish", help="将待办事项标记为已完成", action="store_true")
    set_parser.add_argument("-t", "--title", help="修改待办事项的标题", type=str)
    set_parser.add_argument("-d", "--deadline", help="修改待办事项的截止时间", type=str)
    set_parser.add_argument("-de", "--description", help="修改待办事项的描述", type=str)
    set_parser.add_argument("-l", "--location", help="修改待办事项的地点", type=str)
    set_parser.add_argument("-ta", "--tags", help="修改待办事项的标签", type=str)
    set_parser.add_argument("-r", "--remove", help="删除待办事项", action="store_true")
    
    # 归档待办
    archive_parser.add_argument("id", help="查看id归档的内容，留空则对已完成事项进行归档并简要打印所有已归档事项", default=None, nargs='?')
    
    # 配置
    config_parser.add_argument("-k", "--key", help="设置API Key", type=str)
    config_parser.add_argument("-m", "--model", help="设置使用的模型", type = str)
    config_parser.add_argument("-a", "--api_url", help="设置API请求地址", type=str)
    
    return parser
    
    
def parse_args():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        exit(1)
    return args


def solve(args):
    if args.command == "add":
        if args.auto:
            code, response = todo_agent.ask(args.title)
            if code == 200:
                data_manager.add_todo(eval(response))
                data_manager.save_todos()
                render_todo_item(eval(response))
            else:
                print(f"Error {code}: {response}")
            
        else:
            item = create_todo_item(
                title = args.title,
                description = args.description if args.description else args.title,
                deadline = process_time(args.deadline) if args.deadline else "null",
                tags = args.tags if args.tags else "其他",
                status = "待处理"
            )
            data_manager.add_todo(item)
            data_manager.save_todos()
            render_todo_item(item)
            
    elif args.command == "print":
        if args.id is not None:
            try:
                index = int(args.id) - 1
                todo = data_manager.get_todo(index)
                if todo:
                    render_todo_item(todo)
            except ValueError:
                print("请输入有效的数字ID")
        
        else:
            todos = data_manager.get_all_todos()
            renderer = Renderer(todos)
            renderer.render()
    elif args.command == "set":
        try:
            index = int(args.id) - 1
            todo = data_manager.get_todo(index)
            if not todo:
                return
            
            if args.remove:
                removed = data_manager.remove_todo(index)
                if removed:
                    print(f"已删除事项：{removed['Title']}")
                return
            
            updated_item = todo.copy()
            if args.finish:
                updated_item["Status"] = "已完成"
                from datetime import datetime
                updated_item["CompleteTime"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if args.title:
                updated_item["Title"] = args.title
            if args.deadline:
                standard_time = process_time(args.deadline)
                updated_item["Deadline"] = standard_time
            if args.description:
                updated_item["Description"] = args.description
            if args.location:
                updated_item["Location"] = args.location
            if args.tags:
                updated_item["Tags"] = args.tags
            
            data_manager.set_todo(index, updated_item)
            render_todo_item(updated_item)
            
        except ValueError:
            print("请输入有效的数字ID")
    elif args.command == "archive":
        if args.id is not None:
            try:
                index = int(args.id) - 1
                archived_todo = data_manager.get_todo(index)
                if archived_todo and archived_todo.get("Status") == "已完成":
                    print("归档内容：")
                    render_todo_item(archived_todo)
                else:
                    print("该事项未完成或不存在，无法归档查看。")
            except ValueError:
                print("请输入有效的数字ID")
        else:
            data_manager.archive_todo()
            renderer = Renderer(data_manager.get_archived_todos())
            renderer.render(category="archive")
    elif args.command == "config":
        if args.key:
            config.set_config("api_key", args.key)
            print("API Key 已更新。")
        if args.model:
            config.set_config("model_id", args.model)
            print("模型已更新。")
        if args.api_url:
            config.set_config("base_url", args.api_url)
            print("API请求地址已更新。")
        
        print("当前配置：")
        api_key = config.get_config("api_key") or "未设置"
        model = config.get_config("model_id") or "未设置"
        endpoint = config.get_config("base_url") or "未设置"
        print(f"API Key: {api_key}")
        print(f"模型: {model}")
        print(f"API请求地址: {endpoint}")
        
        
    elif args.command == "help":
        open_help_document()
    else:
        print("未知命令，请使用 'todo help' 查看帮助文档。")

def main():
    check_storage()
    args = parse_args()
    solve(args)
    
if __name__=="__main__":
    main()
    
    
    
    
    



