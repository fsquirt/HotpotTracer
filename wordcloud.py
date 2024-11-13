import pandas as pd
import csv
import datetime
import re
import string
import thulac
from tqdm import tqdm

#n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名 i/习语 j/简称 
useful_word_type = ["n","np","ns","ni","nz","i","j"]
thu1 = thulac.thulac(filt=True)
result_word = []

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

def main():
    global result_word
    print("读取数据")
    #读取热搜数据
    fileHandler = open("hotdata.csv","r",encoding="utf-8")
    fileHandler_line = fileHandler.readlines()
    
    for i in tqdm(fileHandler_line):
        i = i.split(",")
        sentense = i[0] + "," + text_noise_fucker(i[1])
        #https://github.com/thunlp/THULAC-Python?tab=readme-ov-file#%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F
        text = thu1.cut(sentense,text=False)
        for i in text:
            if(i[1] in useful_word_type):
                result_word.append(i[0])  

    print(result_word)

    fileHandler.close()
    
if __name__ == "__main__":
    main()