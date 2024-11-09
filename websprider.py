import requests
import urllib3
import bs4 
import re
import json
from urllib.parse import unquote
import aibasicfun

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        "Priority": "u=0, i",
        "Connection": "keep-alive",
        "Cookie" : """BIDUPSID=BE5530A9823C517F61C20CDFF7DC832F; PSTM=1720807983; BD_UPN=12314753; BDUSS=VFa1F0OUpnODEzQTZsVlJWdUtFUmp-akVYUGdRa0lvVTQxUXNsTWs4Y2Y2dEZtRVFBQUFBJCQAAAAAAQAAAAEAAABBLEcQc2t5a2FsaWxpbnV4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB9dqmYfXapmfm; BDUSS_BFESS=VFa1F0OUpnODEzQTZsVlJWdUtFUmp-akVYUGdRa0lvVTQxUXNsTWs4Y2Y2dEZtRVFBQUFBJCQAAAAAAQAAAAEAAABBLEcQc2t5a2FsaWxpbnV4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB9dqmYfXapmfm; BAIDUID=BE5530A9823C517F9444D73F0405A94A:SL=0:NR=10:FG=1; MCITY=-313%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS_BFESS=61012_60941_61027_61035_61054_60853; H_PS_PSSID=61012_60941_61027_61035_61054_61089_60853_61130_61114_61140; H_WISE_SIDS=61012_60941_61027_61035_61054_61089_60853_61130_61114_61140; BA_HECTOR=218k00a4a10524ak2l8k01251h7l2m1jithh51u; BAIDUID_BFESS=BE5530A9823C517F9444D73F0405A94A:SL=0:NR=10:FG=1; ZFY=NLs03rgrFL11vqNlot:A8N7qAY2KhuWgQQneSkirOjMw:C; BDRCVFR[S4-dAuiWMmn]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=6580v1s%2B%2FXiBsvzSREemmInJdPpVaan1c0XPjzB1aliTUiWMveEdCqp7%2BGEZ7Ew2Eg"""
    }
    
    req = requests.get("https://top.baidu.com/board?tab=realtime",headers=req_header,verify=False,data=None)
    #print(req.status_code)
    
    req.encoding = 'utf-8'
    pattern = r'<!--.*?-->'
    baidu_hotpot = re.findall(pattern, req.text)
    hotpot_oringal = str(baidu_hotpot[0]).replace("<!--s-data:","").replace("-->","")
    htlist = json.loads(hotpot_oringal)
    htlist = htlist["data"]["cards"][0]["content"]
    
    baidu_hotpots = []

    for i in htlist:
        if(i["desc"] == ""):
            req = requests.get(i["rawUrl"],headers=req_header,verify=False,data=None)
            req.encoding = 'utf-8'
            i["desc"] = aibasicfun.ollama_summarize_html(req.text,i["query"])
            i["desc"] = "AI:" + i["desc"]
        #print("热点"+ str(i["index"]) + ":" + i["query"])
        #print("描述:" + str(i["desc"]).replace("\n",""))
        #print("热力指数:" + i["hotScore"])
        #print("url:" + unquote(i["rawUrl"]) + "\n")
        temp_dirc = {"描述:":str(i["desc"]).replace("\n",""),"关键词:":str(i["query"])}
        baidu_hotpots.append(temp_dirc)
    
    print(baidu_hotpots)

if __name__ == '__main__':
    get_baidu_hotpot()



#国外热点追踪
## 获取推特热搜及前十条正文
## 获取BBC各板块的前十条新闻标题及正文
## 获取CNN各板块的前十条新闻标题及正文
## https://cn.wsj.com/ 华尔街日报
## https://m.cn.nytimes.com/ 纽约时报

