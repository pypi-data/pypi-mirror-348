import streamlit as st
# 定义多页面导航

welcome_page = st.Page(
    "pages/1_welcome.py",  # 主入口脚本
    title="欢迎",
    icon=":material/home:"
)
csv_page = st.Page(
    "pages/2_CSV管理.py",  # CSV 管理脚本
    title="CSV 管理",
    icon=":material/folder:"
)
drawing_page = st.Page(
    "pages/3_绘图展板.py",  # 绘图展板脚本
    title="绘图展板",
    icon=":material/palette:"
)
compare_page = st.Page(
    "pages/4_结果对比.py",  # 结果对比脚本
    title="结果对比",
    icon=":material/compare:"
)
pages = [welcome_page, csv_page, drawing_page, compare_page]
pg = st.navigation(pages)



pg.run()
