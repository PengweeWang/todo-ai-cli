from .api import Agent
from .prompt import todo_prompt
from .data import ConfigManager
from .utils import CONFIG_FILE

config = ConfigManager(CONFIG_FILE)

todo_agent = Agent(
    base_url = config.base_url,
    api_key = config.api_key,
    model_id= config.model_id,
    prompt=todo_prompt
)


if __name__=="__main__":
    print(todo_agent.ask("今天中午完成了一场学术会议"))





