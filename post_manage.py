import datetime
import os
import time
from random import randint, random

import JianshuResearchTools as jrt
import streamlit as st

import config
from banword import banword_list
from db_controler import *


def InitDB():
    db = ConnectDatabase("data.db")
    try:
        InitTable(db, "all_post_data")
    except sqlite3.OperationalError:  # 表已存在
        pass
    return db

@st.cache()
def GetNextSortedID(data):
    return data[-1]["sorted_id"]

def comapre_time(source_time, time_limit):
    source_timestamp = time.mktime(source_time)
    source_date = datetime.date.fromtimestamp(source_timestamp)
    return source_date < time_limit


def GetData(island_url, db, table_name, time_limit):
    stop_flag = False
    data_list = jrt.GetIslandPostList(island_url, count=10)  # 首次爬取
    next_sorted_id = GetNextSortedID(data_list)
    AddDataList(db, table_name, data_list)
    for _ in range(10000):
        data_list = jrt.GetIslandPostList(island_url, start_id=next_sorted_id, count=randint(100, 300))
        time.sleep(random())
        new_data_list = []
        for item in data_list:
            if comapre_time(item["create_time"], time_limit):
                new_data_list.append(item)
            else:
                stop_flag += 1  # 帖子不一定按照时间排序，有新评论会导致排序不同
        if data_list != []:
            next_sorted_id = GetNextSortedID(data_list)  # 用原列表获取 ID，防止序号混乱
            AddDataList(db, table_name, new_data_list)
        else:
            break
        if stop_flag >= 5:
            break

def main():
    if config.ISLAND_URL == None:
        st.error("未设置小岛链接")
        return
    db = InitDB()
    
    
    st.header("敏感词检测")
    limit_time = st.date_input("时间限制", help="只会对时间在此之后的帖子进行敏感词检测")
    

    if db.total_changes == 0:
        flag = st.warning("正在获取数据，请稍后......")
        GetData(config.ISLAND_URL, db, "all_post_data", limit_time)
        flag = st.success("获取数据成功！")
    
    cursor = db.execute("SELECT * FROM all_post_data")
    data = cursor.fetchall()
    for item in data:
        content = item[4]
        for word in banword_list:
            if word in content:
                st.write("触发敏感词！" + word + "在内容" + content)
