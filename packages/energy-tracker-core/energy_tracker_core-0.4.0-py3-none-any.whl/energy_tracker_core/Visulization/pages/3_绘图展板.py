import streamlit as st
from energy_tracker_core.Visulization.workspace_task import WorkSpace, Task
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="绘图展板",
    page_icon=":material/palette:",
    layout="wide"
)


st.title("🎨 绘图展板")
ws: WorkSpace = None
ws = st.session_state.get("workspace", None)


def button_callback(task:Task):
    """
    点击按钮后触发回调，设置当前绘图任务
    """

    st.session_state.task_to_plot = task


# 检查前序工作
if 'workspace' not in st.session_state:
    st.warning("请先在 CSV 管理页面初始化工作目录。")
else:
    if 'edited_task_showframe' not in st.session_state:
        st.warning("请先在 CSV 管理页面至少选择一个要分析的csv文件。")
    else:
        # 遍历sw.task_showframe，获取所有选中的任务名称
        selected_task_name = st.session_state.edited_task_showframe.query("is_selected == True")["name"]
        
        # 根据选中的任务名称，获取对应的任务对象,并添加到列表中
        selected_tasks = []
        for task_name in selected_task_name:
            selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
            selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
            selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
        
        # 构造侧边栏切换
        st.sidebar.title("选择任务视图")
        with st.sidebar:
            current_index = None
            for task in selected_tasks:
                st.sidebar.button(task.basic_info["name"], 
                                    key=task.basic_info["name"],
                                    on_click=button_callback,
                                    args=(task,))
        
        if "task_to_plot" not in st.session_state:
            st.markdown("### 请在左侧点击要可视化的任务")
        else:
            task:Task
            task = st.session_state.task_to_plot
            task.analyse()
            st.markdown(f"### 任务名称: {task.basic_info['name']}")
            st.markdown(f"#### 任务路径: {task.csv_filepath}")
            # 创建三列布局
            col1, col2, col3 = st.columns(3)
            
            # 第一列显示基本统计信息
            with col1:
                st.markdown("#### 基本统计")
                st.metric("问答总数", f"{task.statistics['问答总数']}次")
                st.metric("正确率", f"{task.statistics['正确率']:.2%}")
                st.metric("平均每次问答时间", f"{task.statistics['平均每次问答时间(秒)']:.2f}秒")

            # 第二列显示能耗统计
            with col2:
                st.markdown("#### 能耗统计 (Wh)")
                st.metric("总能耗", f"{task.statistics['总能耗(Wh)']:.4f}")
                st.metric("CPU总能耗", f"{task.statistics['CPU总能耗(Wh)']:.4f}")
                st.metric("GPU总能耗", f"{task.statistics['GPU总能耗(Wh)']:.4f}")
                

            # 第三列显示功率统计
            with col3:
                st.markdown("#### 功率统计 (W)")
                st.metric("总平均功率", f"{task.statistics['总平均功率(W)']:.4f}")
                st.metric("CPU平均功率", f"{task.statistics['CPU平均功率(W)']:.4f}")
                st.metric("GPU平均功率", f"{task.statistics['GPU平均功率(W)']:.4f}")
                

            # 创建能耗趋势图
            st.markdown("#### 能耗趋势")
            
            # 创建累计能耗趋势线图
            st.markdown("##### 累计能耗趋势")
            trend_chart_data = pd.DataFrame({
                'CPU累计能耗': task.data['cpu_incremental_energy'].cumsum(),
                'GPU累计能耗': task.data['gpu_incremental_energy'].cumsum(), 
                '总累计能耗': task.data['total_incremental_energy'].cumsum()
            })
            st.line_chart(trend_chart_data)

            # 创建每次问答能耗柱状图
            st.markdown("##### 每次问答能耗")
            bar_chart_data = pd.DataFrame({
                'CPU单次能耗': task.data['cpu_incremental_energy'],
                'GPU单次能耗': task.data['gpu_incremental_energy']
            })
            st.bar_chart(bar_chart_data)

            # 显示能耗最高的问答记录
            st.markdown("#### 能耗最高的问答记录")
            high_energy_df = pd.DataFrame(task.statistics['能耗最高问答'])
            st.dataframe(high_energy_df[['question', 'total_incremental_energy', 'duration']])

            # 显示能耗最低的问答记录
            st.markdown("#### 能耗最低的问答记录") 
            low_energy_df = pd.DataFrame(task.statistics['能耗最低问答'])
            st.dataframe(low_energy_df[['question', 'total_incremental_energy', 'duration']])


# 重置激活页
st.session_state.current_page_index = 3