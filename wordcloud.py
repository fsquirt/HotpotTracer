import pandas as pd
import jieba
import csv
import datetime
import re
import string

def text_noise_fucker(text):
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
    print("读取数据")
    #读取热搜数据
    fileHandler = open("hotdata.csv","r",encoding="utf-8")
    fileHandler_line = fileHandler.readlines()

    result = []
    
    for i in fileHandler_line:
        i = i.split(",")
        sentense = i[0] + "," + text_noise_fucker(i[1])
        text = re.sub(r"[^\w\s]", "", sentense)
        wordlist = jieba.cut(text, HMM=True)
        #filtered_words = [word for word in wordlist if len(word) >= 3]
        result.extend(wordlist)

    print(result)

    fileHandler.close()
    
if __name__ == "__main__":
    main()