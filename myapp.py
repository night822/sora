import streamlit as st
import pandas as pd
import numpy as np
import json

# ==========================================
# 0. 宽屏布局与 Streamlit 官网风 CSS 注入
# ==========================================
st.set_page_config(page_title="SARA-CN 原型", layout="wide")

st.markdown("""
    <style>
    /* 引入极具现代感的 Inter 字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* 隐藏顶部默认红条 */
    /* 精准隐藏右上角 Streamlit 默认菜单和底部水印，保留侧边栏展开按钮 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* 超大号 Hero 标题设计 (大字体核心) */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.05em !important;
        color: #111827 !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        color: #1F2937 !important;
    }

    h3 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* 文本说明放大，增强易读性 */
    p, li {
        font-size: 1.1rem !important;
        color: #374151 !important;
        line-height: 1.6 !important;
    }

    /* 巨型数据指标 (Metric) */
    div[data-testid="stMetricValue"] {
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: #FF4B4B !important; /* Streamlit 标志性亮红色 */
        letter-spacing: -0.05em !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em !important;
        color: #6B7280 !important;
    }

    /* 醒目的胶囊按钮 (Pill Button) */
    div[data-testid="stButton"] button {
        background-color: #FF4B4B !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important; /* 胶囊圆角 */
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(255, 75, 75, 0.39) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6) !important;
    }

    /* 弱化表单边框，使其更融于背景 */
    div[data-testid="stForm"] {
        border: none !important;
        background-color: #F9FAFB !important;
        border-radius: 20px;
        padding: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# 初始化 Session State
if 'baseline_R' not in st.session_state:
    st.session_state['baseline_R'] = 4.2
if 'scenario_data' not in st.session_state:
    st.session_state['scenario_data'] = None

# ==========================================
# 1. 侧边栏导航
# ==========================================
st.sidebar.markdown("### SARA-CN / 导航")
page = st.sidebar.radio(
    "",
    ["项目说明", "场景配置", "风险输入", "结果总览", "缓解对比", "证据导出"],
    label_visibility="collapsed"
)

# ==========================================
# 2. 各页面功能实现
# ==========================================

if page == "项目说明":
    st.title("持续安全风险评估模型")
    st.markdown("### SARA-CN Prototype v1.0")
    st.write("---")

    st.markdown("""
    * **研究边界**：本项目以小型飞机持续运行安全为主线，不作为官方监管认可的审批结论。
    * **版本信息**：v1.0 (离线可用版)
    * **数据标识**：系统严格区分 REAL-A (一手真实)、OFFICIAL-B (官方公开)、PROXY-C (代理数据) 与 SIM-D (仿真数据)。
    """)

elif page == "场景配置":
    st.title("定义运行场景")
    st.markdown("### 设定 CONOPS 核心参数以生成底层计算环境。")
    st.write("---")

    uploaded_file = st.file_uploader("拖拽上传配置文件 (.yaml/.json/.csv)", type=['yaml', 'json', 'csv'])
    if uploaded_file is not None:
        st.success("文件读取成功！")
        st.session_state['scenario_data'] = "已加载"

    with st.form("scenario_form"):
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox("任务类型", ["电动小型固定翼飞行训练", "县域低空货运/应急保障"])
            time_window = st.selectbox("时间窗", ["白天-非高峰", "白天-高峰", "夜间"])
        with col2:
            aircraft_type = st.selectbox("航空器类型", ["RX4E (23类)", "其它小型飞机"])
            data_quality = st.selectbox("数据质量等级", ["REAL-A", "OFFICIAL-B", "PROXY-C", "SIM-D"])

        st.write("")
        submitted = st.form_submit_button("保存配置")
        if submitted:
            st.success(f"已保存：{task_type} 场景")

elif page == "风险输入":
    st.title("参数与权重注入")
    st.markdown("### 配置地面与空中风险场的物理映射规则。")
    st.write("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        ge_weight = st.slider("地面风险 (GE) 权重", 0.0, 1.0, 0.5, 0.1)
        ac_weight = st.slider("空中冲突 (AC) 权重", 0.0, 1.0, 0.5, 0.1)

        if ge_weight + ac_weight != 1.0:
            st.error("权重之和必须为 1.0，请重新调整！")

        st.selectbox("缺失值处理策略", ["使用均值填充", "保留缺失标记并扩大不确定性", "报错并拒绝计算"])

elif page == "结果总览":
    st.title("风险场计算结果")
    st.write("---")

    # 这里的 Metric 会被 CSS 渲染成巨型数字
    col1, col2, col3 = st.columns(3)
    col1.metric("综合风险 R", f"{st.session_state['baseline_R']}")
    col2.metric("地面风险 GE", "3.8")
    col3.metric("空中风险 AC", "4.5")

    st.write("---")
    st.markdown("### 空间热力特征分布")
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [30.65, 104.06],
        columns=['lat', 'lon']
    )
    st.map(map_data)

elif page == "缓解对比":
    st.title("动态干预分析")
    st.markdown("### 测试不同 Mitigation 措施带来的风险降幅与运行代价。")
    st.write("---")

    mitigation_type = st.selectbox(
        "应用控制措施",
        ["无 (基线)", "空间型：避让人口区/固定走廊", "时间型：错峰运行", "数字型：提升 ADS-B 探测"]
    )

    current_R = st.session_state['baseline_R']
    if "时间型" in mitigation_type:
        new_R = current_R - 1.2
    elif "空间型" in mitigation_type:
        new_R = current_R - 0.8
    elif "数字型" in mitigation_type:
        new_R = current_R - 1.5
    else:
        new_R = current_R

    col1, col2 = st.columns(2)
    with col1:
        st.metric("干预后综合风险 R", f"{new_R:.1f}", f"{new_R - current_R:.1f}", delta_color="inverse")

    st.write("---")
    chart_data = pd.DataFrame({
        "基线风险": [current_R] * 10,
        "缓解后风险": [new_R] * 10
    })
    st.line_chart(chart_data)

elif page == "证据导出":
    st.title("证据链生成")
    st.markdown("### 将输入、参数、快照与结论打包为独立审查文件。")
    st.write("---")

    report_dict = {
        "model_version": "v1.0",
        "scenario": "电动小型固定翼飞行训练",
        "baseline_R": st.session_state['baseline_R'],
        "conclusion": "风险在可接受区间内，建议采用时间型错峰缓解措施。"
    }
    report_json = json.dumps(report_dict, ensure_ascii=False, indent=2)

    st.write("")
    st.write("")
    st.download_button(
        label="下载验证报告 (JSON)",
        data=report_json,
        file_name="sara_cn_evidence.json",
        mime="application/json"
    )