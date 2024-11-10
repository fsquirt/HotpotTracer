import aibasicfun
import requests
import websprider
from datetime import datetime

def what_happening():
    print("正在获取正发生")
    
    now = datetime.now()
    current_time = now.strftime("%y/%m/%d-%H:%M:%S")
    print(f"当前时间: {current_time}")
    
    baidu_hotdata = websprider.get_baidu_hotpot()
    weibo_hotdata = websprider.get_weibo_hotpot()
    
    t = 0
    for i in weibo_hotdata:
        #print(str(i["关键词:"]) + "," + str(i["描述:"]).replace(",","，")+ "," +"微博"+ "," +str(t) + "," + str(current_time))
        t = t + 1
        with open("hotdata.csv", mode="a", encoding="utf-8") as file:
            file.write(str(i["关键词:"]) + "," + str(i["描述:"]).replace(",","，")+ "," +"微博"+ "," +str(t) + "," + str(current_time) + "\n")
    
    t = 0
    for i in baidu_hotdata:
        #print(str(i["关键词:"]) + "," + str(i["描述:"]).replace(",","，")+ "," +"百度"+ "," +str(t) + "," + str(current_time))
        t = t + 1
        with open("hotdata.csv", mode="a", encoding="utf-8") as file:
            file.write(str(i["关键词:"]) + "," + str(i["描述:"]).replace(",","，")+ "," +"百度"+ "," +str(t) + "," + str(current_time) + "\n")

def frist_init():
    print("开始初始化")
    aibasicfun.init_global()
    what_happening()

if __name__ == '__main__':
    frist_init()