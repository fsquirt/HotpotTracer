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
frist_write = True

#获取小标题
def get_news_title(text):
    matches = re.findall(r"【(.*?)】", text)
    if(len(matches) == 0):
        return ""
    else:
        return matches[0]

def main():
    global frist_write
    global writed_news_latest_id
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
        if(temp_latest_id == writed_news_latest_id):
            pass
        else:
            #print("有更新")
            for i in news_data:
                if(i["id"] == writed_news_latest_id):
                    break
                
                #【小标题】 小标题处理
                print(i["rich_text"])
                little_title = get_news_title(i["rich_text"])
                if(i != ""):
                    i["rich_text"] = re.sub(r"【.*?】", "", i["rich_text"])

                #正文内容半角换全角
                i["rich_text"] = str(i["rich_text"]).replace(",", "，")
                
                #写入文件，使得第一行是最新内容
                with open("sinarealtime.csv","r+", encoding="utf-8") as file:
                    content = file.read()
                    file.seek(0)
                    file.write(str(i["id"]) + "," + str(i["create_time"]) + ","  + little_title + "," + i["rich_text"] + "\n" + content)
                    
            writed_news_latest_id = temp_latest_id
            
        time.sleep(10)

if __name__ == '__main__':
    main()