import pandas as pd
import csv
import datetime
import re
import string
import thulac
from tqdm import tqdm
from collections import Counter

#n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名 i/习语 j/简称 
useful_word_type = ["n","np","ns","ni","nz","i","j"]
thu1 = thulac.thulac(filt=True)
result_word = []

#词云黑名单
black_word_list = ["网友", "公司","消息", "集团", "时间", "科技", "经济","市场", "政策", "数据", "机构", "产品", "全球", "问题", "热议", "有限公司","粉丝","产品","机构", "指数", "市场", "政府", "新闻", "股份", "视频", "计划", "信息", "行业", "日本", "国际", "部门", "风险","媒体", "需求", "人士","记者","风险","企业", "领域", "产业", "能源", "水平", "报告","业务", "目标", "资本", "微博","金融", "关系", "平台", "投资者", "业务","证券", "技术","事件", "态度", "官方", "行为", "作品", "男子", "当事方","原因","话题"]

def text_noise_fucker(text):
    #去除噪声 没啥用 thulac有这功能 加上也不影响
    try:
        text_list = str(text).split("，")
        if((text_list[0] == "近日") or text_list[0] == "近期"):
            return str(text)[3:]   
        else:
            pattern = r"\d+月\d+日，"
            pattern2 = r"\d+日，"
            pattern3 = r"\d+月\d+日上午，"
            pattern4 = r"\d+月\d+日傍晚，"
            pattern5 = r"\d+月\d+日下午，"
            pattern6 = r"\d+月\d+日深夜，"

            result = re.sub(pattern, "", text)
            result = re.sub(pattern2, "", result)
            result = re.sub(pattern3, "", result)
            result = re.sub(pattern4, "", result)
            result = re.sub(pattern5, "", result)
            result = re.sub(pattern6, "", result)
            result = result.replace(" ","")
            
            return result
    except:
        return text.replace(" ","")
    
def analyze_hot_search_data():
    global result_word
    fileHandler = open("hotdata.csv","r",encoding="utf-8")
    fileHandler_line = fileHandler.readlines()
    
    print("处理热搜数据")
    for i in tqdm(fileHandler_line):
        i = i.split(",")
        sentense = i[0] + "," + text_noise_fucker(i[1])
        #https://github.com/thunlp/THULAC-Python?tab=readme-ov-file#%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F
        text = thu1.cut(sentense,text=False)
        temp_list = []
        for i in text:
            if(i[1] in useful_word_type):
                temp_list.append(i[0])  
                
        #去重先 有噪声
        unique_lst = pd.Series(temp_list).unique().tolist()
        for i in unique_lst:
            result_word.append(i)
        
    fileHandler.close()
    
def analyze_7x24_data():
    global result_word
    fileHandler = open("sinarealtime.csv","r",encoding="utf-8")
    fileHandler_line = fileHandler.readlines()
    
    print("处理财经7x24小时新闻数据")
    for i in tqdm(fileHandler_line):
        i = i.split(",")
        if(len(i) == 4):
            sentense = i[2] + "," + text_noise_fucker(i[3])
        else:
            sentense = i[2]
        text = thu1.cut(sentense,text=False)
        temp_list = []
        for i in text:
            if(i[1] in useful_word_type):
                temp_list.append(i[0])  

        #去重先 有噪声
        unique_lst = pd.Series(temp_list).unique().tolist()
        for i in unique_lst:
            result_word.append(i)

    fileHandler.close()

def count_duplicates(lst):
    global black_word_list
    # 统计每个元素的出现次数
    count = Counter(lst)
    
    # 按照出现次数从大到小排序
    sorted_count = count.most_common()
    top_word_list = []
    temp_counter = 0
    
    # 输出结果
    for item, freq in sorted_count:
        if(temp_counter >= 30):
            break
        if(freq > 1) and (len(item) >= 2) and (item not in black_word_list):  # 只输出重复的元素
            print(f"{item}, {freq}")
            print("加入词云:" + item)
            top_word_list.append(item)
            temp_counter = temp_counter + 1
        
    print(top_word_list)
    

def main():
    print("读取数据")
    analyze_hot_search_data()
    #analyze_7x24_data()
    print(result_word)
    count_duplicates(result_word)
    
if __name__ == "__main__":
    main()