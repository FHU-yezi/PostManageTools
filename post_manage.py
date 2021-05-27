import time
from random import randint, random

import JianshuResearchTools as jrt
import streamlit as st

import config
from banword import banword_list
from db_controler import *


def InitDB():
    db = ConnectDatabase("data.db")
    InitTable(db, "all_post_data")
    return db

@st.cache()
def GetNextSortedID(data):
    return data[-1]["sorted_id"]


def GetData(island_url, db, table_name, day_limit):
    stop_flag = False
    data_list = jrt.GetIslandPostList(island_url, count=10)  # 首次爬取
    next_sorted_id = GetNextSortedID(data_list)
    AddDataList(db, table_name, data_list)
    for _ in range(10000):
        data_list = jrt.GetIslandPostList(island_url, start_id=next_sorted_id, count=randint(100, 300))
        time.sleep(random())
        new_data_list = []
        for item in data_list:
            if item["create_time"].tm_mday > day_limit:
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
        return
    try:
        db = InitDB()
    except Exception:
        pass

    if db.total_changes == 0:
        flag = st.warning("正在获取数据，请稍后......")
        GetData(config.ISLAND_URL, db, "all_post_data", 26)
        flag = st.success("获取数据成功！")
    
    cursor = db.execute("SELECT * FROM all_post_data")
    data = cursor.fetchall()
    for item in data:
        content = item[4]
        for word in banword_list:
            if word in content:
                st.write("触发敏感词！" + word + "在内容" + content)
