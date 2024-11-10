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
            i["desc"] = aibasicfun.ollama_summarize_html_baidu(req.text,i["query"])
            i["desc"] = "AI:" + i["desc"]
        #print("热点"+ str(i["index"]) + ":" + i["query"])
        #print("描述:" + str(i["desc"]).replace("\n",""))
        #print("热力指数:" + i["hotScore"])
        #print("url:" + unquote(i["rawUrl"]) + "\n")
        temp_dirc = {"描述:":str(i["desc"]).replace("\n",""),"关键词:":str(i["query"])}
        baidu_hotpots.append(temp_dirc)
    
    print(baidu_hotpots)
    return baidu_hotpots
    
def get_weibo_hotpot():
    weibo_header = {
        "Cookie": "XSRF-TOKEN=HK6Q9FClbkDAzP5vr0laU22o; SCF=Au8xBk4YckYe7JWAMapHOYhkVoM51dJXjBL0cdXtOmBYFoo_dkF8Eqj5L4J1ZPdbb0fkE2_8x91VHPS8zpSZ8b0.; SUB=_2A25KNBT9DeRhGeFK61AU-SrFyTqIHXVpSCg1rDV8PUNbmtAGLVDjkW9NQ7EcQYZZLtj8WXFpwXWabVZG2rSfSTze; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvYDNdpV2BXkfTQjjKkbup5NHD95QNSh5ESK.X1KzcWs4Dqcjci--ci-zEiK.4i--ci-ihi-27i--NiKnpi-z7i--fiKnpiKLWi--4i-2EiK.Ri--fi-88i-zc; ALF=02_1733816751; _s_tentry=passport.weibo.com; Apache=7720083282596.335.1731224775174; SINAGLOBAL=7720083282596.335.1731224775174; ULV=1731224775177:1:1:1:7720083282596.335.1731224775174:; WBPSESS=iCPQ2msLZgwMRitkN7q-S-YlUbGx_iPrWO4h_3hxOFBqoI1fxri4PevHtWmUy6EYjwa5RYkNT_7tiPVkSJBke9EX6e7paUxAThRLgb_2oQaIQK9dk_7rMXZT8KctDWHajcZnaSDtE-P_UkQW08_qUw==",
        "Sec-Ch-Ua-Platform": "Windows",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Server-Version": "v2024.11.04.1",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Client-Version": "v2.46.27",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://weibo.com/",
        "Priority": "u=1, i"
    }
    
    weibo_hotpots = []
    
    req = requests.get("https://weibo.com/ajax/side/searchBand?type=hot&last_tab=hot",headers=weibo_header,verify=False)
    req.encoding = 'utf-8'
    weibo_hot_orginal = json.loads(req.text)
    weibo_hot_orginal = weibo_hot_orginal["data"]["realtime"]
    for i in weibo_hot_orginal:
        desc_req = requests.get(str("https://s.weibo.com/weibo?q=" + i["word"]),headers=weibo_header,verify=False)
        desc_req.encoding = 'utf-8'
        #print(desc_req.text)
        weibo_desc_temp = aibasicfun.ollama_summarize_html_weibo(desc_req.text,i["word"])
        #print(i["word"] + " " + weibo_desc_temp)
        temp_dirc = {"描述:":weibo_desc_temp.replace("\n",""),"关键词:":str(i["word"])}
        weibo_hotpots.append(temp_dirc)

    print(weibo_hotpots)
    return weibo_hotpots

if __name__ == '__main__':
    get_weibo_hotpot()