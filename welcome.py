import streamlit as st
import config

def main():
    st.write("欢迎来到简书小岛管理平台！")
    if config.ISLAND_URL == None:
        st.write("请转到“设置”页面，填写小岛链接。")