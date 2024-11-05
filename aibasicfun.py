import requests
import ollama
import random
from datetime import datetime
import sys
import pyautogui
import psutil
import logging


logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 设置时间格式
)

proxies = {
  "http": "http://127.0.0.1:10809",
  "https": "http://127.0.0.1:10809",
}

module_config ={
    ## https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values
    "mirostat" : 0, #启用 Mirostat 采样以控制困惑度。（默认：0，0 = 禁用，1 = Mirostat，2 = Mirostat 2.0）
    "mirostat_eta" : 0.1,#影响算法对生成文本反馈的响应速度。较低的学习率会导致调整速度变慢，而较高的学习率会使算法更加灵敏。（默认：0.1）
    "mirostat_tau" : 5.0, #控制输出之间的连贯性和多样性之间的平衡。较低的值将导致文本更加专注和连贯。（默认：5.0）
    "num_ctx num_ctx" : 2048,#设置用于生成下一个标记的上下文窗口的大小。（默认：2048）
    "repeat_last_n" : 64 , #设置模型回溯多远以防止重复。（默认：64，0 = 禁用，-1 = num_ctx）
    "repeat_penalty" : 1.1, #设置重复的惩罚强度。更高的值（例如，1.5）将更强烈地惩罚重复，而更低的值（例如，0.9）将更加宽容。（默认：1.1）
    "temperature" : 0.7, #模型温度。提高温度会使模型回答更具创造性。（默认：0.8）
    "seed" : random.randint(1,sys.maxsize) #设置用于生成的随机数种子。将此设置为特定数字将使模型对相同的提示生成相同的文本。（默认：0）
}

# 初始化
def init_global():
    logging.info("初始化随机数生成器")
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y%m%d%H%M%S')
    x, y = pyautogui.position()
    threads_count = sum([p.num_threads() for p in psutil.process_iter()])
    base_seed = int((int(formatted_time)/int(threads_count)) * (x + y))
    logging.info("强随机种子:" + str(base_seed))
    random.seed(base_seed)
    
    if(check_proxy() == 1):
        return 1
    if(test_ollama() == 1):
        return 1
    
    ollama_translate(1,"你说得对，但是《原神》是由上海米哈游网络科技股份有限公司制作发行的一款开放世界冒险游戏，游戏发生在一个被称作“提瓦特”的幻想世界，在这里，被神选中的人将被授予“神之眼”，导引元素之力。玩家将扮演一位名为“旅行者”的神秘角色，在自由的旅行中邂逅性格各异、能力独特的同伴们，和他们一起击败强敌，找回失散的亲人——同时，逐步发掘“原神”的真相。")
    ollama_translate(2,"Make American Great Again!")
    
    return 0

## 与ollama本地服务端通信
def test_ollama():
    try:
        response = ollama.generate(model='qwen2.5', prompt='注意：不要生成markdown! 下面是问题:你是谁？',options=module_config)
        logging.info(response["response"])
        
        response = ollama.generate(model='qwen2.5', prompt='注意：不要生成markdown! 下面是问题:你有没有感情？',options=module_config)
        logging.info(response["response"])
        return 0
    except:
        logging.info("ollama服务未启动")
        return 1

## 检测代理设置
def check_proxy():
    try:
        res1 = requests.get('https://www.google.com/',proxies=proxies)
        res2 = requests.get('http://www.google.com/', proxies=proxies)
        if (res1.status_code == 200) and (res2.status_code == 200):
            logging.info("代理设置正常")
            return 0
        else:
            logging.info("代理设置异常")
            return 1
    except:
        logging.info("代理设置异常")
        return 1

#基本功能
## 调用ollama进行英译中
def ollama_translate(tran_type,text):
    #tran_type 1 中译英 2 英译中
    if(tran_type == 1):
        prompt = '你是一位翻译助理，现在需要你发挥你的工作能力，将下面的中文文本翻译成地道的英文，注意不要加入任何自然语言，这是你要翻译的中文文本:' + text
        logging.info(prompt)
        response = ollama.generate(model='qwen2.5',prompt=prompt,options=module_config)
        logging.info(response["response"])
        return response["response"]
    if(tran_type == 2):
        prompt = '你是一位翻译助理，现在需要你发挥你的工作能力，将下面的英文文本翻译成地道的中文，注意不要加入任何自然语言，这是你要翻译的英文文本:' + text
        logging.info(prompt)
        response = ollama.generate(model='qwen2.5',prompt=prompt,options=module_config)
        logging.info(response["response"])
        return response["response"]
    
## 根据长文本生成一句话概括
def ollama_summarize(text):
    prompt = '你是一位阅读专家，现在需要你发挥你的工作能力，分析要点将下面的段落概括成100字左右，注意不要加入任何自然语言，这是你要总结的段落:' + text
    response = ollama.generate(model='qwen2.5',prompt=prompt,options=module_config)
    restext = response["response"]
    logging.info("调用ollama生成概括:" + restext)
    return restext


