import requests
import json


class Agent:
    def __init__(self, base_url:str, api_key:str, model_id:str, prompt:str):
        self.base_url = base_url
        self.api_key = api_key
        self.model_id = model_id
        self.prompt = prompt
        
    def ask(self, content: str) -> tuple[int, str]:
        try:
            # 构建请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # 构建请求体，将系统提示和用户内容结合
            payload = {
                "model": self.model_id,
                "messages": [
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": content}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # 发送POST请求
            response = requests.post(
                url=self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30  # 设置超时时间，避免无限等待
            )
            
            # 检查响应状态码
            response.raise_for_status()
            
            # 解析JSON响应
            result = response.json()
            
            # 提取返回的内容（根据常见的API响应格式）
            if "choices" in result and len(result["choices"]) > 0:
                return 200, result["choices"][0]["message"]["content"]
            else:
                return 500, "API返回格式不符合预期"
                
        except requests.exceptions.HTTPError as e:
            # 处理HTTP错误（如401认证失败、404未找到等）
            status_code = e.response.status_code if e.response else 500
            return status_code, f"HTTP错误: {str(e)}"
        except requests.exceptions.ConnectionError:
            # 处理连接错误
            return 503, "连接错误: 无法连接到API服务器"
        except requests.exceptions.Timeout:
            # 处理超时错误
            return 408, "超时错误: API请求超时"
        except json.JSONDecodeError:
            # 处理JSON解析错误
            return 500, "解析错误: 无法解析API返回的JSON"
        except Exception as e:
            # 处理其他未知错误
            return 500, f"未知错误: {str(e)}"
        
        
    
class Qweather:
    def __init__(self, api_host, token):
        self.api_host = api_host
        self.token = token
        
    def query_weather(self, loc):
        ...
        
    
    def query_loc(self, name):
        ... 
        
        





