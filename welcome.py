import streamlit as st
import config

def main():
    if config.DEBUG_MODE == True:
        st.warning("调试模式已启用")
        
    st.write("欢迎来到简书小岛管理中心！")
    if config.ISLAND_URL == "":
        st.write("请转到“设置”页面，填写小岛链接")