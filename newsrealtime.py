import requests
import json
import time
import re

sina_header = {
    "Cookie": "ALF=02_1733816752; SCF=Au8xBk4YckYe7JWAMapHOYhkVoM51dJXjBL0cdXtOmBYkoDj_VBf6GnIngesHu0e3DM73d1ArfKsYwvw0_EV6L8.; SUB=_2A25KNBTgDeRhGeFK61AU-SrFyTqIHXVpSCgorDV_PUJbkNB-LRb5kW9NQ7EcQSFZSKMndXIBRhk4_pLb0Kqkckwh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvYDNdpV2BXkfTQjjKkbup5NHD95QNSh5ESK.X1KzcWs4Dqcjci--ci-zEiK.4i--ci-ihi-27i--NiKnpi-z7i--fiKnpiKLWi--4i-2EiK.Ri--fi-88i-zc; UOR=,finance.sina.com.cn,; ULV=1731412294581:1:1:1::; SINAGLOBAL=218.17.105.17_1731412274.172461; Apache=218.17.105.17_1731412274.172462; U_TRS1=00000091.eb52864f.6733413d.eddd69db; U_TRS2=00000091.eb5a864f.6733413d.0816f558",
    "Sec-Ch-Ua-Platform": "Windows",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
    "Referer": "https://finance.sina.com.cn/"
}

writed_news_latest_id = 0

def get_news_title(text):
    #获取小标题
    matches = re.findall(r"【(.*?)】", text)
    if(len(matches) == 0):
        return ""
    else:
        return matches[0]
    
def read_latest_id():
    #获取最新ID 如果获取不到，那就是第一次写数据，第一次请求的数据就会都写上
    global writed_news_latest_id
    try:
        with open("id.txt","r",encoding="utf-8") as file:
            writed_news_latest_id = int(file.read())
    except:
        writed_news_latest_id = 0

def main():
    global writed_news_latest_id
    read_latest_id()
    
    while(True):
        url = "https://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery1112032572744792696806_1731412294007&page=1&page_size=20&zhibo_id=152&tag_id=0&dire=f&dpc=1&pagesize=20&id=3868085&"
        req = requests.get(url)
        req.encoding = "utf-8"
        req_json = str(req.text)[47:-14]
        req_json = json.loads(req_json)
        sina_server_time = req_json["result"]["timestamp"]
        temp_latest_id = req_json["result"]["data"]["feed"]["list"][0]["id"]
        news_data = req_json["result"]["data"]["feed"]["list"]
        print("当前服务器时间:" + str(sina_server_time) + "   最新ID：" + str(temp_latest_id))
        #判断有无内容更新
        if(temp_latest_id <= writed_news_latest_id):
            #如果获取到的最新ID小于等于已经写入的最新ID 那就是没有更新
            pass
        else:
            for i in news_data:
                if(i["id"] <= writed_news_latest_id):
                    #一直写 直到要写的新闻ID小于等于已经写入的ID 那就是这条新闻已经写进去了 于是退出循环
                    break
                
                #【小标题】 小标题处理
                print(i["rich_text"])
                little_title = get_news_title(i["rich_text"])
                if(i != ""):
                    i["rich_text"] = re.sub(r"【.*?】", "", i["rich_text"])
                
                #半角换全角 去掉回车
                i["rich_text"] = str(i["rich_text"]).replace(",","，")
                i["rich_text"] = str(i["rich_text"]).replace("\n","")
                
                #写入文件
                with open("sinarealtime.csv","a+", encoding="utf-8") as file:
                    if(little_title != ""):
                        file.write(str(i["id"]) + "," + str(i["create_time"]) + ","  + little_title + "," + i["rich_text"] + "\n")
                    else:
                        file.write(str(i["id"]) + "," + str(i["create_time"]) + "," + i["rich_text"] + "\n")
                    
            writed_news_latest_id = temp_latest_id
            #更新最新ID
            with open("id.txt","w",encoding="utf-8") as file:
                file.write(str(writed_news_latest_id))
            
        time.sleep(30)

if __name__ == '__main__':
    main()