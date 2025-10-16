from setuptools import setup, find_packages

setup(
    name="todo-ai",
    version="0.1.0",
    description="一个带AI能力的命令行待办事项管理工具",
    author="PonyWee",
    packages=find_packages(),
    package_data={
        "todo": ["help.html"]  # 格式：{包名: [文件名列表]}
    },
    install_requires=[
        "requests>=2.31.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "todo = todo.todo:main",  # 命令行入口，对应 todo.py 的 main 函数
        ]
    },
    python_requires=">=3.8"
)