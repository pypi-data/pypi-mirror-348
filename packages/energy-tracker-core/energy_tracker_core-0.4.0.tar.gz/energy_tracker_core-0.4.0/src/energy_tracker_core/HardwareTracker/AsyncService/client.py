# client_http_client.py
import time
import http.client
from typing import Callable
import urllib.parse
import uuid

def _post(token: str, path: str, host: str="127.0.0.1", port: int=8000, data: dict={}):
    # 1. 序列化为 x-www-form-urlencoded
    body = urllib.parse.urlencode(data)
    # 2. 建立连接
    conn = http.client.HTTPConnection(host, port)
    # 3. 发送 POST
    conn.request(
        method="POST",
        url=path,
        body=body,
        headers={
            "Token": token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    # 4. 获取响应
    resp = conn.getresponse()
    print(f"Status: {resp.status} {resp.reason}")
    text = resp.read().decode('utf-8', errors='ignore')
    print("Body:\n", text)
    conn.close()

def _start_inference_by_token(token: str, question: str):
    _post(token, "/start_inference", data={"question": question})

def _stop_inference_by_token(token: str, answer: str, is_correct: bool, is_valid: bool):
    _post(token, "/stop_inference", data={"answer": answer, "is_correct": is_correct, "is_valid": is_valid})

class Trace:
    def __init__(self):
        self.token = str(uuid.uuid4())

    def start_inference(self, question: str):
        _start_inference_by_token(self.token, question)

    def stop_inference(self, answer: str, is_correct: bool, is_valid: bool):
        _stop_inference_by_token(self.token, answer, is_correct, is_valid)

    def refresh_token(self):
        self.token = str(uuid.uuid4())
        return self.token
    
def determine_function(question: str, answer: str) -> bool:
    return True
def validate_function(question: str, answer: str) -> bool:
    return True

def tracker_with_correction(determine_function: Callable[[str, str], bool]=determine_function, validate_function: Callable[[str, str], bool]=validate_function):
    def decorator(func: Callable[[str], str]):
        trace = Trace()
        def wrapper(question: str):
            # 开始记录能耗
            trace.start_inference(question)
            
            # 执行原函数
            answer = func(question)
            
            # 判断是否正确以及合规
            is_correct = determine_function(question,answer)
            is_valid = validate_function(question,answer)
            # 停止记录能耗
            trace.stop_inference(answer, is_correct, is_valid)  
            
            return answer
        
        return wrapper

    return decorator






if __name__ == "__main__":
    @tracker_with_correction(determine_function, validate_function)
    def test_function(question: str) -> str:
        time.sleep(5)
        return "Hello, World!"
    # 示例调用
    while True:
        test_function("Hello?")
        time.sleep(10)




