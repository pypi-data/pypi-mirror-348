import streamlit as st


st.set_page_config(
    page_title="欢迎/帮助",
    page_icon="🏠",
    layout="centered"
)
st.title("🎉 欢迎使用CSV Visulization! 🏠")

st.markdown(
    """
    ### 本项目为Energy Tracker的子项目, 用于可视化能耗追踪服务日志
    ### 使用说明
    - 请使用左侧侧边栏切换至对应功能页面。
    - 在各功能页面，根据提示输入或选择参数，页面将自动渲染结果。
    - 目前支持csv日志管理, 单个日志可视化和多日志对比。

    ### 快捷操作
    - Windows: `Ctrl+R` 重载页面
    - macOS: `⌘+R` 重载页面

    ### 联系方式
    有任何问题，请联系：philippe.qu@outlook.com
    """
)

st.info("当前为欢迎/帮助页面，可在侧边栏选择其他页面。")
st.session_state.current_page_index = 1