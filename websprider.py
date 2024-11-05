import requests
import urllib3
import bs4 
import re

# 百度热搜
def get_baidu_hotpot():
    req_header = {
        "Sec-Ch-Ua": """"Not?A_Brand";v="99", "Chromium";v="130""",
        "Sec-Ch-Ua-Platform": "Windows",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive"
    }
    
    req = requests.get("https://top.baidu.com/board?tab=realtime",headers=req_header,verify=False,data=None)
    req.encoding = 'utf-8'
    print(req.text)
    pattern = r'<!--.*?-->'
    baidu_hotpot = re.findall(pattern, req.text)


if __name__ == '__main__':
    get_baidu_hotpot()




#国外热点追踪
## 获取推特热搜及前十条正文
## 获取BBC各板块的前十条新闻标题及正文
## 获取CNN各板块的前十条新闻标题及正文
## https://cn.wsj.com/ 华尔街日报
## https://m.cn.nytimes.com/ 纽约时报

