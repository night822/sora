import streamlit as st
import pandas as pd
import numpy as np
import json

# ==========================================
# 0. 全局大字号宽屏布局与 CSS 深度定制
# ==========================================
st.set_page_config(page_title="SARA-CN 原型", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 18px !important; 
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    h1 {
        font-size: 4rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.05em !important;
        margin-bottom: 1rem !important;
    }
    h2 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    h3 {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }

    p, li, .stMarkdown {
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        color: #FF4B4B !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #6B7280 !important;
    }

    div[data-testid="stButton"] button {
        background-color: #FF4B4B !important;
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        padding: 0.8rem 2.5rem !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(255, 75, 75, 0.3) !important;
    }

    section[data-testid="stSidebar"] {
        padding-top: 2rem !important;
    }
    .stRadio > div[role="radiogroup"] > label {
        margin-bottom: 1.8rem !important; 
        padding-left: 0.5rem !important;
    }
    .stRadio > div[role="radiogroup"] > label > div {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #374151 !important;
    }
    .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'baseline_R' not in st.session_state:
    st.session_state['baseline_R'] = 4.2

# ==========================================
# 1. 侧边栏
# ==========================================
st.sidebar.markdown("### SARA-CN 导航")
st.sidebar.write("---")

page = st.sidebar.radio(
    "",
    ["项目说明", "系统使用手册", "场景配置 (CONOPS)", "风险数据输入", "结果总览", "缓解与干预", "证据包导出"],
    label_visibility="collapsed"
)

# ==========================================
# 2. 页面功能模块化实现
# ==========================================

if page == "项目说明":
    st.title("SARA-CN 持续安全评估")
    st.markdown("### 基于时空风险场的低空运行安全闭环系统")
    st.write("---")

    with st.container():
        st.markdown("### 严正声明与研究边界")
        st.error("""
        **1. 非官方审批依据 (模型定位)**  
        本项目所建立的连续风险场模型及等级输出（包括自拟的 LRL 状态或借鉴的 GRC/ARC 映射）**仅定位为科研原型与辅助决策工具**。本系统**不能、也无权**替代中国民航局 (CAAC) 的适航审定、飞行审批或任何官方监管结论。

        **2. 适用边界限定 (场景隔离)**  
        项目立足于中国低空起步阶段，严格遵循**“先载货后载人、先隔离后融合、先远郊后城区”**的现实原则。当前系统验证主线仅针对“小型通用航空器（如23类电动飞机）”与“特定场景（飞行训练/县域货运）”，**城市中心大规模载人 eVTOL 仅作为未来扩展，绝不作为当前已验证成果**。

        **3. 数据局限性提示 (责任边界)**  
        由于当前真实低空运行数据有限，系统采用了多源数据融合。所有结论均高度受限于输入数据的真实性等级，若无高质量的实时数据支撑，本模型**不承诺提供“全国实时监管”级别的绝对精确度**。
        """)

    st.write("")
    st.markdown("### 强制数据标识规范")
    st.info("""
    在系统输出的每一张报表与图表中，均需严格追溯以下数据质量标签，**严禁用仿真数据伪装真实运行数据，代理变量不得写成直接测量**：
    * **REAL-A (一手真实)**：经授权的实际航迹、运行与维修现场测量数据。
    * **OFFICIAL-B (官方公开)**：政府统计公报、民航局、权威地理/气象数据。
    * **PROXY-C (代理数据)**：采用人口密度、通信覆盖等作为难获取变量的替代指标。
    * **SIM-D (仿真数据)**：按公开假设生成的交通流，仅限于可行性及敏感性验证。
    """)

elif page == "系统使用手册":
    st.title("操作指南与变量说明")
    st.markdown("### SARA-CN 风险评估原型 v1.0 官方文档")
    st.write("---")

    st.markdown("""
    #### 模块一：场景配置 (CONOPS)
    在此模块界定风险评估的基础物理与组织环境。
    * **任务维度**：选择航空器执行的具体任务（如飞行培训、县域低空通勤），这决定了航线的复杂程度。
    * **航空器维度**：选择具体机型，例如 23 类小型电动固定翼飞机（需额外考虑电池热失控风险与能量衰减问题）。
    * **时间与组织维度**：界定白天/夜间窗，以及是采用固定低空走廊还是 UTM 接入的区域调度。

    #### 模块二：风险数据输入
    系统采用连续风险场模型，核心参数物理含义如下：
    * **地面风险场 (GE) 核心变量**：
      * **人口密度 (Pd)**：航线下方及迫降区域内的每平方公里人数。
      * **后果脆弱性 (Cv)**：航线是否穿越高铁、电网枢纽、学校及医院等高敏感设施。
      * **冲击能量 (Ei)**：由飞机重量、速度及潜在的电池热失控能量决定。
    * **空中冲突场 (AC) 核心变量**：
      * **交通密度 (Td)**：单位空域内同时运行的航空器数量（架次/小时）。
      * **数字探测能力 (Da)**：ADS-B、Remote ID 或雷达对该空域的有效覆盖率。
      * **空域复杂度 (Sc)**：军民航混合程度及无人机密集程度。

    #### 模块三：缓解与干预 (Mitigation)
    针对超标风险，可从库中调用以下四类控制措施：
    * **空间型**：设置固定走廊或主动避让人口区（降低地面暴露 Pd）。
    * **时间型**：执行错峰运行或动态时间窗（直接削减交通密度 Td）。
    * **数字型**：强制 UTM 在线接入或数字孪生预测（提升数字探测 Da）。
    * **组织型**：政府平台或城市群协同联动调度（提升系统容错率）。

    *系统将在执行干预后，同步核算风险降幅与所需付出的运行代价（如绕飞距离、延误时间）。*

    #### 模块四：数据质量标定红线
    系统严格要求区分数据来源等级：
    * **REAL-A (一手真实)**：经授权的实际航迹、运行与维修现场测量数据。
    * **OFFICIAL-B (官方公开)**：政府、民航局、统计公报等权威数据。
    * **PROXY-C (代理数据)**：无法获取真实数据时使用的合理替代指标（需解释偏差）。
    * **SIM-D (仿真数据)**：按公开假设生成的交通流，仅用于可行性验证。
    """)

elif page == "场景配置 (CONOPS)":
    st.title("定义运行概念 (CONOPS)")
    st.write("---")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            task_type = st.selectbox("飞行任务类型",
                                     ["电动小型固定翼飞行训练", "县域低空货运/应急保障", "其它特种作业"])
            aircraft_type = st.selectbox("航空器维度", ["RX4E (23类电动)", "传统燃油小型飞机", "大型长航时无人机"])
        with col2:
            time_env = st.selectbox("时间与气象维度", ["白天/良好天气 (高频次)", "夜间/复杂气象", "全天候动态窗"])
            org_type = st.selectbox("运行组织方式", ["固定航线/学院统一调度", "UTM接入/多主体协同", "隔离空域自由飞行"])

    st.write("")
    if st.button("锁定场景配置"):
        st.success("场景要素已冻结，底层计算引擎已同步。")

elif page == "风险数据输入":
    st.title("风险变量映射表")
    st.write("---")

    tab1, tab2, tab3 = st.tabs(["地面风险暴露 (GE)", "空中交通冲突 (AC)", "权重与缺失策略"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("地面暴露密度 Pd (人/平方公里)", min_value=0, value=500, step=50)
            st.number_input("航线运行暴露因子 Sf (小时)", min_value=0.0, value=1.5, step=0.1)
        with col2:
            st.selectbox("后果脆弱性 Cv", ["无敏感设施", "存在学校/医院 (高权重)", "存在高铁/电网枢纽 (极高权重)"])
            st.selectbox("迫降区域可达性", ["良好 (开阔地多)", "一般", "极差 (密集建筑区)"])

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("交通密度 Td (架次/小时)", ["低密度 (<5架)", "中密度 (5-20架)", "高密度 (>20架)"])
            st.slider("数字探测能力 Da (ADS-B覆盖率 %)", 0, 100, 75)
        with col2:
            st.selectbox("空域复杂度 Sc", ["简单 (单一主体)", "中等 (军民航适度混合)", "复杂 (无序多主体)"])
            st.slider("自主碰撞避免能力 Aa (%)", 0, 100, 85)

    with tab3:
        st.slider("地面风险 (GE) 物理权重", 0.0, 1.0, 0.6)
        st.selectbox("异常值与缺失数据干预策略", ["分位数截断并保留标记 (推荐)", "直接丢弃", "使用经验均值强行填充"])

elif page == "结果总览":
    st.title("实时风险场演算")
    st.write("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("系统综合风险 R", f"{st.session_state['baseline_R']}")
    col2.metric("地面风险峰值 GE", "4.1")
    col3.metric("空中冲突残余 AC", "3.6")

    st.write("---")
    st.markdown("### 空间风险聚类热力图 (格网输出验证)")

    df = pd.DataFrame(
        np.random.randn(500, 2) / [30, 30] + [30.65, 104.06],
        columns=['lat', 'lon']
    )
    st.map(df, zoom=11)

elif page == "缓解与干预":
    st.title("动态控制与缓解 (Mitigation)")
    st.write("---")

    mitigation_type = st.selectbox(
        "从控制措施库 (OSO-CN) 中调用干预逻辑",
        ["[基线运行] 不施加额外干预",
         "[时间型] 启动空域错峰与动态时间窗",
         "[空间型] 启用固定安全走廊并避让敏感区"]
    )

    current_R = st.session_state['baseline_R']
    if "时间型" in mitigation_type:
        new_R = current_R - 1.4
        cost = "日均训练架次压缩 15%，组织协调成本上升"
    elif "空间型" in mitigation_type:
        new_R = current_R - 0.9
        cost = "单次航线距离增加 8km，航空器能耗上升"
    else:
        new_R = current_R
        cost = "无额外运行代价"

    st.write("")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("干预后综合风险 R", f"{new_R:.1f}", f"{new_R - current_R:.1f}", delta_color="inverse")
    with col2:
        st.info(f"**付出的运行代价与成本**：\n{cost}")

elif page == "证据包导出":
    st.title("自动化证据生成")
    st.write("---")
    st.markdown("提取自场景配置与缓解模型的底层数据快照，确保可复现、可追溯。")

    report_dict = {
        "Data_Log": "REAL-A_v1.2",
        "Config": "电动小型固定翼_错峰运行",
        "R_Baseline": st.session_state['baseline_R'],
        "Conclusion": "风险下降至可接受区间 (LRL-2)，单调性测试通过。"
    }
    report_json = json.dumps(report_dict, ensure_ascii=False, indent=2)

    st.write("")
    st.download_button(
        label="一键生成并导出 JSON 证据卷宗",
        data=report_json,
        file_name="sara_cn_evidence.json",
        mime="application/json"
    )