import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- 網頁基本設定 ---
st.set_page_config(page_title="金融情報預警平台", layout="wide")

# --- 系統狀態管理 ---
if 'page' not in st.session_state:
    st.session_state.page = "戰情總覽與處置矩陣"
if 'target_account' not in st.session_state:
    st.session_state.target_account = "ACCT_8839_A1"

def set_page():
    st.session_state.page = st.session_state.sidebar_radio

def jump_to_investigate(account_id):
    st.session_state.target_account = account_id
    st.session_state.page = "單一帳戶深度調查"

# --- 擴充模擬資料庫 ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        '帳戶代碼': [
            'ACCT_8839_A1', 'ACCT_3345_B2', 'ACCT_7721_C3', 'ACCT_9910_D4', 
            'ACCT_1122_E5', 'ACCT_4432_A1', 'ACCT_6654_B2', 'ACCT_2211_C3', 
            'ACCT_5512_C3', 'ACCT_1024_D4'
        ],
        '所屬機構': ['A銀行', 'B銀行', 'C銀行', 'D銀行', 'E銀行', 'A銀行', 'B銀行', 'C銀行', 'A銀行', 'C銀行'],
        '近2日交易筆數': [45, 52, 38, 60, 15, 18, 12, 10, 5, 3],
        '近2日轉入總額': [2500000, 3200000, 1800000, 4500000, 1000, 500, 2000, 0, 50000, 15000],
        '近2日轉出總額': [2495000, 3190000, 1790000, 4495000, 500, 100, 0, 0, 45000, 10000],
        '當前餘額': [5000, 10000, 10000, 5000, 1500, 1200, 2000, 800, 25000, 55000],
        '風險指數': [98, 95, 93, 91, 88, 85, 82, 78, 45, 12],
        '案件狀態': [
            '🔴 觸發處置_建議圈存', '🔴 觸發處置_建議圈存', '🔴 觸發處置_建議圈存', '🔴 觸發處置_建議圈存', 
            '🟡 高風險觀察_持續監控', '🟡 高風險觀察_持續監控', '🟡 高風險觀察_持續監控', '🟡 高風險觀察_持續監控', 
            '🟢 正常_背景監控', '🟢 正常_背景監控'
        ]
    })

df = load_data()

# --- 側邊欄：系統導覽 ---
st.sidebar.title("金融情報預警平台")
st.sidebar.caption("國家級異常資金流分析核心")
st.sidebar.markdown("---")

pages = ["戰情總覽與處置矩陣", "模型庫與資料匯入測試", "單一帳戶深度調查", "國家級情報聯防網路"]
st.sidebar.radio("系統功能模組", pages, index=pages.index(st.session_state.page), key="sidebar_radio", on_change=set_page)

st.sidebar.markdown("---")
st.sidebar.write("**登入身分:** 系統管理員")
st.sidebar.write("**當前掛載機制:** 假投資防堵專用版")
st.sidebar.write("**觀測視窗:** 2 日內動態")

# ==========================================
# 頁面 1：戰情總覽與處置矩陣
# ==========================================
if st.session_state.page == "戰情總覽與處置矩陣":
    st.title("戰情總覽與風險處置矩陣")
    st.markdown("依據「前置行為觀察」與「資金突增觸發」兩階段邏輯，精準調控銀行防堵力道。")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="今日掃描交易總筆數", value="159,543", delta="12% 增長")
    col2.metric(label="高風險觀察名單 (列管中)", value="4", delta="🟡 待查核")
    col3.metric(label="觸發處置名單 (大額流入)", value="4", delta="🔴 需立即圈存", delta_color="inverse")
    col4.metric(label="系統誤報干擾率", value="0.24%", delta="精準度極高", delta_color="normal")
    
    st.markdown("---")
    
    st.markdown("### 自動化風險分級處置準則 (兩階段防堵機制)")
    st.table(pd.DataFrame({
        '風險區間': ['> 90分 (🔴 觸發處置)', '75 - 89分 (🟡 高風險觀察)', '< 75分 (🟢 正常)'],
        '行為特徵狀態': ['列管中帳戶突然「動起來」：出現大額異常流入，並準備快速移轉', '出現前置洗錢行為 (如長久靜止戶突有小額測試、跨國IP頻繁登入)，但尚未有大筆資金', '行為落於常態分布範圍內'],
        '系統自動處置建議': ['發布【圈存通報】，建議銀行立即圈存該筆匯入款，防止車手提領', '發布【觀察通知】，建議銀行對該戶加強查核與持續監控，不輕易鎖卡', '寫入背景監控日誌']
    }))

    st.markdown("---")
    
    colA, colB = st.columns(2)
    with colA:
        st.subheader("🟡 高風險觀察清單 (列管中)")
        st.caption("偵測到前置異常行為，已通報銀行注意，等待資金觸發。")
        monitor_df = df[df['案件狀態'].str.contains('🟡')].reset_index(drop=True)
        
        for index, row in monitor_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([4, 3, 3])
                c1.write(f"**{row['帳戶代碼']}**\n({row['所屬機構']})")
                c2.write(f"風險: {row['風險指數']}分")
                c3.button("🔎 深度調查", key=f"btn_y_{index}", on_click=jump_to_investigate, args=(row['帳戶代碼'],), use_container_width=True)
                st.divider()

    with colB:
        st.subheader("🔴 觸發處置清單 (需圈存)")
        st.caption("列管帳戶已開始接收大額資金，準備洗出，需立即攔截！")
        action_df = df[df['案件狀態'].str.contains('🔴')].reset_index(drop=True)
        
        for index, row in action_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([4, 3, 3])
                c1.write(f"**{row['帳戶代碼']}**\n({row['所屬機構']})")
                c2.write(f"風險: {row['風險指數']}分")
                c3.button("🚨 執行處置", key=f"btn_r_{index}", on_click=jump_to_investigate, args=(row['帳戶代碼'],), use_container_width=True)
                st.divider()

# ==========================================
# 頁面 2：模型庫與資料匯入測試 
# ==========================================
elif st.session_state.page == "模型庫與資料匯入測試":
    st.title("防詐策略庫與資料接收測試")
    st.markdown("因應詐欺集團手法演進，系統支援掛載最新防禦策略，並可隨時進行資料驗證。")
    
    st.subheader("1. 選擇當前防堵策略")
    model_col1, model_col2 = st.columns([2, 1])
    with model_col1:
        selected_model = st.selectbox(
            "請選擇要掛載的偵測引擎：",
            [
                "🟢 [最新] 假投資特化版 (預測成功率: 86.47% | 本月更新)",
                "🟡 [通用] 跨行聯合防禦版 (預測成功率: 81.87% | 上季更新)",
                "⚪ [歷史] 基礎洗錢防制版 (預測成功率: 80.68% | 去年更新)"
            ]
        )
    with model_col2:
        st.info("💡 **架構優勢**：我們能根據詐騙手法的改變，隨時更新防禦邏輯，不影響前線業務。")

    st.markdown("---")
    
    st.subheader("2. 模擬資料接收測試")
    tab_api, tab_upload = st.tabs(["🔌 銀行系統即時連線測試", "📁 本機歷史案件上傳測試"])
    
    with tab_api:
        st.markdown("模擬接收來自各合作銀行端點的即時連線資料。")
        api_col1, api_col2 = st.columns(2)
        with api_col1:
            st.text_input("連線通道 (API URL)", value="https://api.cib.gov.tw/v1/fraud-radar", disabled=True)
        with api_col2:
            st.text_input("安全金鑰", value="sk-xxxxxxxxxxxxxxxxxxxx", type="password")
        
        if st.button("🔌 模擬啟動即時監控", type="primary"):
            with st.spinner(f"正在套用最新防堵策略進行解析..."):
                time.sleep(1)
                st.code('系統狀態: 接收資料中... 處理筆數: 54 筆', language='text')
                time.sleep(1)
                st.code('系統狀態: 分析2日內交易特徵... 完成', language='text')
                time.sleep(1.5)
            st.success("測試通過！成功攔截 2 筆高風險交易，已自動推播至戰情總覽。")

    with tab_upload:
        st.markdown("用於歷史案件回溯，或讓尚未完成系統連線的銀行進行批次驗證。")
        uploaded_file = st.file_uploader("請上傳去識別化交易紀錄 (CSV/Excel 格式)", type=['csv', 'xlsx'])
        
        if uploaded_file is not None or st.button("執行批次案件掃描", type="primary"):
            with st.spinner(f"正在掃描資料並套用最新防堵策略..."):
                time.sleep(2)
            st.success("掃描完成！")
            
            st.markdown("#### 📊 測試報告摘要")
            report_col1, report_col2, report_col3 = st.columns(3)
            report_col1.metric("解析資料筆數", "15,420 筆")
            report_col2.metric("抓出潛在洗錢帳戶", "8 戶")
            report_col3.metric("系統信心水準", "94.2%")

# ==========================================
# 頁面 3：單一帳戶深度調查 
# ==========================================
elif st.session_state.page == "單一帳戶深度調查":
    st.title("單一帳戶深度調查")
    
    account_list = df['帳戶代碼'].tolist()
    default_idx = account_list.index(st.session_state.target_account) if st.session_state.target_account in account_list else 0
    
    selected_account = st.selectbox("當前調查目標帳戶：", account_list, index=default_idx)
    account_info = df[df['帳戶代碼'] == selected_account].iloc[0]
    
    is_red = '🔴' in account_info['案件狀態']
    is_yellow = '🟡' in account_info['案件狀態']
    
    st.subheader(f"監控目標狀態：{selected_account} ({account_info['案件狀態']})")
    col_a, col_b, col_c = st.columns(3)
    col_a.write(f"**所屬機構:** {account_info['所屬機構']}")
    col_b.write(f"**當前餘額:** {account_info['當前餘額']:,} TWD")
    col_c.write(f"**風險指數:** {account_info['風險指數']}")
    
    st.markdown("---")
    
    if is_red or is_yellow:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["資金關聯圖譜", "異常行為解析", "動態行為時間軸", "登入軌跡分析", "自動生成公文"])
        
        with tab1:
            if is_red:
                st.markdown("⚠️ **【階段二：大額洗錢運作中】** 資金節點已出現「高頻匯入」與「快速分流」。")
                nodes = [
                    f"{{name: '未確認關係人 A\\n(大額匯入)', itemStyle: {{color: '#4A6984'}}}}",
                    f"{{name: '目標帳戶\\n{selected_account}', itemStyle: {{color: '#A03232'}}, symbolSize: 85}}",
                    f"{{name: '疑似分流帳戶 C\\n(極速轉出)', itemStyle: {{color: '#D48A41'}}}}"
                ]
                links = [
                    f"{{source: '未確認關係人 A\\n(大額匯入)', target: '目標帳戶\\n{selected_account}', label: {{show: true, formatter: '觸發圈存點'}}}}",
                    f"{{source: '目標帳戶\\n{selected_account}', target: '疑似分流帳戶 C\\n(極速轉出)', label: {{show: true, formatter: '準備分流'}}}}"
                ]
            else:
                st.markdown("⚠️ **【階段一：前置準備期】** 該帳戶目前僅有小額測試與零星金流，已被系統打上觀察標籤。")
                nodes = [
                    f"{{name: '異常來源 (小額測試)', itemStyle: {{color: '#4A6984'}}}}",
                    f"{{name: '觀察帳戶\\n{selected_account}', itemStyle: {{color: '#D48A41'}}, symbolSize: 85}}"
                ]
                links = [
                    f"{{source: '異常來源 (小額測試)', target: '觀察帳戶\\n{selected_account}', label: {{show: true, formatter: '測試連通性'}}}}"
                ]

            graph_html = f"""
            <!DOCTYPE html><html><head><script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script></head>
            <body style="margin:0; padding:0;"><div id="main" style="width: 100%; height: 400px;"></div>
            <script>
                var chart = echarts.init(document.getElementById('main'));
                chart.setOption({{
                    series: [{{
                        type: 'graph', layout: 'force', symbolSize: 60, roam: true,
                        label: {{ show: true, fontSize: 13, color: '#fff' }},
                        edgeSymbol: ['none', 'arrow'], edgeSymbolSize: [4, 10], force: {{ repulsion: 1000, edgeLength: 200 }},
                        data: [{','.join(nodes)}],
                        links: [{','.join(links)}],
                        lineStyle: {{ width: 2, curveness: 0.1, color: '#666' }}
                    }}]
                }});
            </script></body></html>
            """
            components.html(graph_html, height=420)

        with tab2:
            st.markdown("系統偵測到以下異常行為，這是推升風險分數的主要原因：")
            shap_data = pd.DataFrame({
                '異常行為特徵': ['近3日單筆最大金額突增', '近3日轉入資金過度集中', '轉帳間隔時間極短 (不像真人)', '單日轉出次數過於頻繁', '帳戶餘額有刻意清空跡象'],
                '嚴重程度': [0.94, 0.85, 0.72, 0.45, 0.31] if is_red else [0.21, 0.15, 0.82, 0.11, 0.65]
            }).sort_values(by='嚴重程度', ascending=True)
            st.bar_chart(shap_data.set_index('異常行為特徵'), color="#8B0000" if is_red else "#D48A41")

        with tab3:
            now = datetime.now()
            if is_red:
                st.info(f"**(數日前)**：帳戶出現小額測試，列入【🟡 高風險觀察清單】")
                st.error(f"**T=0 ({(now - timedelta(minutes=15)).strftime('%H:%M')})**：系統偵測到大額資金 {account_info['近2日轉入總額']:,} 元突然匯入！")
                st.error(f"**T+5 分鐘 ({(now - timedelta(minutes=10)).strftime('%H:%M')})**：風險分數飆升至 {account_info['風險指數']}分。系統發布【🔴 圈存通報】。")
            else:
                st.warning(f"**T=0 ({(now - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M')})**：休眠帳戶突然出現異常連線與微量匯款。")
                st.warning(f"**目前狀態**：列入【🟡 高風險觀察清單】，等待資金流入觸發處置機制。")

        with tab4:
            st.markdown("### 🌍 數位足跡與連線位置分析")
            map_data = pd.DataFrame({'lat': [25.0330, 11.5564], 'lon': [121.5654, 104.9282], 'size': [100, 500], 'color': ['#0000FF', '#FF0000']})
            st.map(map_data, zoom=3, use_container_width=True)
            st.caption("🔴 紅點表示異常的境外登入位置 (如：東南亞地區)，🔵 藍點為客戶原本常態活動的地區。")

        with tab5:
            st.markdown("### 📄 自動生成公文")
            if is_red:
                official_doc = f"""發文機關：內政部警政署刑事警察局 (情報聯防中心)
受文者：{account_info['所屬機構']} 法遵與風控部
主旨：有關貴機構帳戶 {selected_account} 出現重大異常資金流入，建請即刻執行「預防性圈存」，請查照。
說明：
一、該帳戶日前已被本系統列為高風險觀察對象。今日系統偵測其匯入 {account_info['近2日轉入總額']:,} 元，洗錢風險極高。
二、為防止車手將資金轉出，建請貴機構對該筆資金啟動「預防性圈存(Hold)」，本局將接續進行深入調查。"""
            else:
                official_doc = f"""發文機關：內政部警政署刑事警察局 (情報聯防中心)
受文者：{account_info['所屬機構']} 法遵與風控部
主旨：有關貴機構帳戶 {selected_account} 出現前置異常行為，建請列入「加強監控對象」，請查照。
說明：
一、本系統偵測該帳戶近期行為軌跡（如IP跳轉、頻率異常）極度吻合洗錢前置特徵。
二、建請貴機構對該戶加強盡職審查(EDD)。若後續有異常大額資金匯入，請配合本系統之二次通報進行阻斷。"""
            
            st.code(official_doc, language="markdown")

    else:
        st.success("行為腳本判定：未檢測出顯著之洗錢特徵，持續背景監控。")

# ==========================================
# 頁面 4：國家級情報聯防網路 (全白話文版)
# ==========================================
elif st.session_state.page == "國家級情報聯防網路":
    st.title("🌐 跨機構情報整合：打通數據孤島")
    
    st.markdown("""
    ### 解決跨行合作的最大痛點：如何在「不碰到個資」的前提下共享情報？
    過去我們推動跨行聯防，最大的阻力就是「銀行不能交出客戶名單與交易明細」。
    
    我們未來的解法是：**讓各家銀行自己關起門來算，只把「算出來的詐騙手法特徵」交給刑事局。**
    
    也就是說，A 銀行發現了新的洗錢手法，他們不需要把被害人或車手的名字交出來，只要把這個「手法的特徵規律」傳給情報中心。情報中心整合後，再把這個新招式的「防禦疫苗」發給全台灣所有銀行。
    這樣一來，既沒有個資外洩的風險，又能做到**「一家被騙，全台免疫」**。
    """)
    
    st.markdown("---")
    st.subheader("🛠️ 模擬：跨行情報整合與派發")
    
    if st.button("🚀 啟動防詐情報大串連", type="primary"):
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            with st.spinner("A 銀行分析中..."):
                time.sleep(1.5)
            st.success("A銀行：已攔截新型態洗錢手法，正將「特徵規律」回傳給刑事局。")
        with col_y:
            with st.spinner("B 銀行分析中..."):
                time.sleep(2)
            st.success("B銀行：日常防禦經驗回傳中...")
        with col_z:
            with st.spinner("C 銀行分析中..."):
                time.sleep(1.8)
            st.success("C銀行：日常防禦經驗回傳中...")
            
        st.info("🔄 刑事局情報中心：正在整合各行回傳的特徵，製作最新版「防禦大腦」...")
        time.sleep(1.5)
        st.success("✅ **整合完畢！最新防禦機制已同步派發給全台銀行，預警成功率提升至 89.5%！**")
    
    st.markdown("---")
    
    fed_html = """
    <!DOCTYPE html><html><head><script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script></head>
    <body style="margin:0; padding:0;"><div id="main" style="width: 100%; height: 450px;"></div>
    <script>
        var chart = echarts.init(document.getElementById('main'));
        chart.setOption({
            backgroundColor: '#0E1117',
            series: [{
                type: 'graph', layout: 'none', symbolSize: 70,
                label: { show: true, color: '#fff', fontSize: 14, position: 'bottom' },
                data: [
                    {name: '刑事局情報中心\\n(統整詐騙特徵)', x: 500, y: 300, itemStyle: {color: '#A03232'}, symbolSize: 100},
                    {name: 'A銀行\\n(客戶資料留存本地)', x: 200, y: 150, itemStyle: {color: '#4A6984'}},
                    {name: 'B銀行\\n(客戶資料留存本地)', x: 800, y: 150, itemStyle: {color: '#4A6984'}},
                    {name: 'C銀行\\n(客戶資料留存本地)', x: 200, y: 450, itemStyle: {color: '#4A6984'}},
                    {name: 'D銀行\\n(客戶資料留存本地)', x: 800, y: 450, itemStyle: {color: '#4A6984'}}
                ],
                links: [
                    {source: 'A銀行\\n(客戶資料留存本地)', target: '刑事局情報中心\\n(統整詐騙特徵)'},
                    {source: 'B銀行\\n(客戶資料留存本地)', target: '刑事局情報中心\\n(統整詐騙特徵)'},
                    {source: 'C銀行\\n(客戶資料留存本地)', target: '刑事局情報中心\\n(統整詐騙特徵)'},
                    {source: 'D銀行\\n(客戶資料留存本地)', target: '刑事局情報中心\\n(統整詐騙特徵)'}
                ],
                lineStyle: { color: '#555', width: 2 }
            }, {
                type: 'lines', coordinateSystem: 'cartesian2d', polyline: true,
                effect: { show: true, period: 3, trailLength: 0.2, symbol: 'arrow', symbolSize: 10, color: '#00FA9A' },
                lineStyle: { width: 0 },
                data: [
                    {coords: [[200, 150], [500, 300]]}, {coords: [[800, 150], [500, 300]]},
                    {coords: [[200, 450], [500, 300]]}, {coords: [[800, 450], [500, 300]]}
                ]
            }]
        });
    </script></body></html>
    """
    components.html(fed_html, height=470)