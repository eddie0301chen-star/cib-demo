import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- 網頁基本設定 ---
st.set_page_config(page_title="金融情報預警平台", layout="wide")

# --- 系統狀態管理 (用於跨頁面跳轉) ---
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
        '帳戶代碼': ['ACCT_8839_A1', 'ACCT_3345_B2', 'ACCT_7721_C3', 'ACCT_9910_D4', 'ACCT_1122_E5', 'ACCT_5512_C3', 'ACCT_1024_D4', 'ACCT_4432_A1', 'ACCT_6654_B2', 'ACCT_9921_E5'],
        '所屬機構': ['A銀行', 'B銀行', 'C銀行', 'D銀行', 'E銀行', 'A銀行', 'C銀行', 'A銀行', 'B銀行', 'B銀行'],
        '近2日交易筆數': [45, 52, 38, 60, 25, 12, 3, 5, 2, 8],
        '近2日轉入總額': [2500000, 3200000, 1800000, 4500000, 950000, 50000, 15000, 8000, 3000, 12000],
        '近2日轉出總額': [2495000, 3190000, 1790000, 4495000, 940000, 45000, 10000, 5000, 1000, 8000],
        '當前餘額': [5000, 10000, 10000, 5000, 10000, 25000, 55000, 3000, 2000, 150000],
        '風險指數': [98, 95, 92, 88, 85, 45, 12, 9, 5, 8],
        '案件狀態': [
            '🔴 待處置_極高風險', '🔴 待處置_極高風險', '🔴 待處置_極高風險', 
            '🟡 已發文_圈存監控中', '🟡 已發文_圈存監控中', '🟢 背景監控', 
            '🟢 正常', '🟢 正常', '🟢 正常', '🟢 正常'
        ]
    })

df = load_data()

# --- 側邊欄：系統導覽 ---
st.sidebar.title("金融情報預警平台")
st.sidebar.caption("國家級異常資金流分析核心")
st.sidebar.markdown("---")

# 使用 Session State 控制的選單
pages = ["戰情總覽與處置矩陣", "跨機構資料匯入", "單一帳戶深度調查", "跨機構聯邦學習架構"]
st.sidebar.radio("系統功能模組", pages, index=pages.index(st.session_state.page), key="sidebar_radio", on_change=set_page)

st.sidebar.markdown("---")
st.sidebar.write("**登入身分:** 系統管理員")
st.sidebar.write("**核心演算法:** XGBoost")
st.sidebar.write("**觀測視窗:** 2 日區塊")

# ==========================================
# 頁面 1：戰情總覽與處置矩陣 (擴充雙清單與跳轉)
# ==========================================
if st.session_state.page == "戰情總覽與處置矩陣":
    st.title("戰情總覽與風險處置矩陣")
    st.markdown("基於「事前阻斷」戰略，追蹤待處置之高風險帳戶，與已發布公文之圈存帳戶狀態。")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="今日掃描交易總筆數", value="159,543", delta="12% 增長")
    col2.metric(label="高風險待處置帳戶", value="3", delta="建議立即圈存", delta_color="inverse")
    col3.metric(label="圈存監控中帳戶", value="2", delta="已發文防堵")
    col4.metric(label="系統誤報率 FPR", value="0.24%", delta="極低干擾", delta_color="normal")
    
    st.markdown("---")
    
    colA, colB = st.columns(2)
    with colA:
        st.subheader("🔴 待處置：高風險監控清單")
        st.caption("AI 判定為洗錢高風險，尚未發布警示通報，建議立即調查。")
        pending_df = df[df['案件狀態'] == '🔴 待處置_極高風險'].reset_index(drop=True)
        
        # 建立帶有跳轉按鈕的列表
        for index, row in pending_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.write(f"**{row['帳戶代碼']}** ({row['所屬機構']})")
                c2.write(f"風險: {row['風險指數']}分")
                c3.button("🔎 深度調查", key=f"btn_p_{index}", on_click=jump_to_investigate, args=(row['帳戶代碼'],))
                st.divider()

    with colB:
        st.subheader("🟡 追蹤中：已圈存/監控清單")
        st.caption("已發布預防性圈存公文，持續監控後續異常轉帳或收款行為。")
        monitoring_df = df[df['案件狀態'] == '🟡 已發文_圈存監控中'].reset_index(drop=True)
        
        for index, row in monitoring_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.write(f"**{row['帳戶代碼']}** ({row['所屬機構']})")
                c2.write(f"風險: {row['風險指數']}分")
                c3.button("🔎 追蹤動態", key=f"btn_m_{index}", on_click=jump_to_investigate, args=(row['帳戶代碼'],))
                st.divider()

# ==========================================
# 頁面 2：跨機構資料匯入
# ==========================================
elif st.session_state.page == "跨機構資料匯入":
    st.title("跨機構資料匯入與特徵萃取")
    st.file_uploader("匯入交易紀錄 CSV 檔", type=['csv', 'xlsx'])
    if st.button("啟動 AI 特徵運算與風險評估", type="primary"):
        with st.spinner("執行時間區塊回溯與特徵萃取中..."):
            time.sleep(2)
        st.success("批次資料分析完成，請至戰情總覽檢視高風險節點。")

# ==========================================
# 頁面 3：單一帳戶深度調查
# ==========================================
elif st.session_state.page == "單一帳戶深度調查":
    st.title("單一帳戶深度調查 (預防性分析)")
    
    # 預設選中從上一頁傳來的 target_account
    account_list = df['帳戶代碼'].tolist()
    default_idx = account_list.index(st.session_state.target_account) if st.session_state.target_account in account_list else 0
    
    selected_account = st.selectbox("當前調查目標帳戶：", account_list, index=default_idx)
    account_info = df[df['帳戶代碼'] == selected_account].iloc[0]
    
    st.subheader(f"監控目標狀態：{selected_account} ({account_info['案件狀態']})")
    col_a, col_b, col_c = st.columns(3)
    col_a.write(f"**所屬機構:** {account_info['所屬機構']}")
    col_b.write(f"**當前餘額:** {account_info['當前餘額']:,} TWD")
    col_c.write(f"**AI 風險指數:** {account_info['風險指數']}")
    
    st.markdown("---")
    
    if account_info['風險指數'] > 80:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["資金關聯圖譜", "特徵歸因 SHAP", "動態行為時間軸", "IP 地理軌跡", "預防性圈存公文"])
        
        with tab1:
            st.markdown("資金節點呈現典型之**「多進多出、快速分流」**特徵。*(註：因尚未有報案紀錄，資金來源標示為高風險關係人)*")
            graph_html = f"""
            <!DOCTYPE html><html><head><script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script></head>
            <body style="margin:0; padding:0;"><div id="main" style="width: 100%; height: 450px;"></div>
            <script>
                var chart = echarts.init(document.getElementById('main'));
                chart.setOption({{
                    series: [{{
                        type: 'graph', layout: 'force', symbolSize: 60, roam: true,
                        label: {{ show: true, fontSize: 13, color: '#fff' }},
                        edgeSymbol: ['none', 'arrow'], edgeSymbolSize: [4, 10], force: {{ repulsion: 1000, edgeLength: 150 }},
                        data: [
                            {{name: '未確認關係人 A\\n(異常匯入)', itemStyle: {{color: '#4A6984'}}}},
                            {{name: '未確認關係人 B\\n(異常匯入)', itemStyle: {{color: '#4A6984'}}}},
                            {{name: '監控中帳戶\\n{selected_account}', itemStyle: {{color: '#A03232'}}, symbolSize: 85}},
                            {{name: '疑似分流帳戶 C\\n(極速轉出)', itemStyle: {{color: '#D48A41'}}}},
                            {{name: '外部資金池', itemStyle: {{color: '#526A54'}}}}
                        ],
                        links: [
                            {{source: '未確認關係人 A\\n(異常匯入)', target: '監控中帳戶\\n{selected_account}', label: {{show: true, formatter: '高頻匯入'}}}},
                            {{source: '未確認關係人 B\\n(異常匯入)', target: '監控中帳戶\\n{selected_account}', label: {{show: true, formatter: '高頻匯入'}}}},
                            {{source: '監控中帳戶\\n{selected_account}', target: '疑似分流帳戶 C\\n(極速轉出)', label: {{show: true, formatter: '多層化分流'}}}},
                            {{source: '疑似分流帳戶 C\\n(極速轉出)', target: '外部資金池', label: {{show: true, formatter: '資金移轉'}}}}
                        ],
                        lineStyle: {{ width: 2, curveness: 0.1, color: '#666' }}
                    }}]
                }});
            </script></body></html>
            """
            components.html(graph_html, height=470)

        with tab2:
            st.markdown("模型決策權重解析：量化各項行為特徵對推升風險指數之貢獻度。")
            shap_data = pd.DataFrame({
                '特徵指標': ['近3日最大交易金額 (F10)', '近3日轉入總金額 (F14)', '最短交易時間間隔 (F3)', '近3日轉出次數 (F21)', '單筆交易金額 (F8)'],
                '貢獻度權重': [0.94, 0.75, 0.62, 0.55, 0.31]
            }).sort_values(by='貢獻度權重', ascending=True)
            st.bar_chart(shap_data.set_index('特徵指標'), color="#8B0000")

        with tab3:
            st.markdown("### ⏱️ 2 日觀測視窗內之異常操作節奏")
            now = datetime.now()
            st.info(f"**T=0 ({(now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')})**：未確認關係人 A 匯入 1,000,000 元")
            st.warning(f"**T+12 分鐘 ({(now - timedelta(hours=1, minutes=48)).strftime('%H:%M')})**：未確認關係人 B 匯入 1,500,000 元")
            st.error(f"**T+25 分鐘 ({(now - timedelta(hours=1, minutes=35)).strftime('%H:%M')})**：網銀將 1,200,000 轉至疑似分流帳戶 (觸發最短時間間隔異常)")
            
            if account_info['案件狀態'] == '🟡 已發文_圈存監控中':
                st.success(f"**T+30 分鐘 ({(now - timedelta(hours=1, minutes=30)).strftime('%H:%M')})**：🛡️ **成功觸發圈存機制，剩餘 1,300,000 元已遭凍結，後續轉出失敗。**")
            else:
                st.error(f"**T+45 分鐘 ({(now - timedelta(minutes=75)).strftime('%H:%M')})**：餘額降至極低 (觸發資金清空特徵，亟需處置)")

        with tab4:
            st.markdown("### 🌍 數位足跡與 IP 地理軌跡分析")
            map_data = pd.DataFrame({'lat': [25.0330, 24.1477, 11.5564], 'lon': [121.5654, 120.6736, 104.9282], 'size': [100, 100, 500], 'color': ['#0000FF', '#0000FF', '#FF0000']})
            st.map(map_data, zoom=3, use_container_width=True)

        with tab5:
            st.markdown("### 📄 自動生成：金融機構預防性圈存通報")
            official_doc = f"""發文機關：內政部警政署刑事警察局 (情報聯防中心)
受文者：{account_info['所屬機構']} 法遵與風控部
主旨：有關貴機構帳戶 {selected_account} 出現重大異常資金流動，建請即刻執行「預防性圈存」與加強監控，請查照。
說明：
一、依據「國家級金融情報預警系統」動態行為分析，該帳戶近 2 日內資金操作呈極高風險（AI 評分：{account_info['風險指數']} 分）。
二、經查該帳戶尚未有報案紀錄，然其行為高度吻合洗錢特徵。於 2 日內異常匯入 {account_info['近2日轉入總額']:,} 元，並於極短時間內密集轉出。
三、建請貴機構針對該帳戶當前餘額 {account_info['當前餘額']:,} 元先行啟動預防性圈存(Hold)，本局將接續進行深入調查。"""
            st.code(official_doc, language="markdown")

    else:
        st.success("行為腳本判定：未檢測出顯著之洗錢特徵，持續背景監控。")

# ==========================================
# 頁面 4：跨機構聯邦學習架構 (實體操作版)
# ==========================================
elif st.session_state.page == "跨機構聯邦學習架構":
    st.title("🌐 跨機構聯邦學習架構 (Federated Learning)")
    
    st.markdown("""
    ### 什麼是「聯邦學習」？為什麼我們需要它？
    在過去，銀行因為《個資法》的限制，無法將客戶資料交給警方或其他銀行比對，導致「詐欺情報破碎化」。
    **聯邦學習（Federated Learning）** 是突破此困境的核心技術：**「數據不動，模型動」**。各銀行只在自家內部訓練 AI，然後將不含任何個資的「數學參數（特徵權重）」上傳給情報中心。情報中心匯總後，再把更聰明的 AI 大腦派發給全體銀行。
    """)
    
    st.markdown("---")
    st.subheader("🛠️ 啟動參數交換模擬")
    
    if st.button("🚀 啟動今日聯邦學習參數聚合 (Global Aggregation)", type="primary"):
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            with st.spinner("A 銀行本地端訓練中..."):
                time.sleep(1.5)
            st.success("A 銀行：發現新型態快進快出特徵，權重參數已加密匯出。")
        with col_y:
            with st.spinner("B 銀行本地端訓練中..."):
                time.sleep(2)
            st.success("B 銀行：本地參數已加密匯出。")
        with col_z:
            with st.spinner("C 銀行本地端訓練中..."):
                time.sleep(1.8)
            st.success("C 銀行：本地參數已加密匯出。")
            
        st.info("🔄 刑事局 AI 大腦正在進行參數聚合 (Federated Averaging)...")
        time.sleep(1.5)
        st.success("✅ **全局模型更新完成！全台銀行已同步具備防禦最新詐欺手法之能力。全域 F1-Score 提升至 89.5%！**")
    
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
                    {name: 'CIB 中央 AI 大腦\\n(僅接收權重參數)', x: 500, y: 300, itemStyle: {color: '#A03232'}, symbolSize: 100},
                    {name: 'A銀行\\n(保有原始個資)', x: 200, y: 150, itemStyle: {color: '#4A6984'}},
                    {name: 'B銀行\\n(保有原始個資)', x: 800, y: 150, itemStyle: {color: '#4A6984'}},
                    {name: 'C銀行\\n(保有原始個資)', x: 200, y: 450, itemStyle: {color: '#4A6984'}},
                    {name: 'D銀行\\n(保有原始個資)', x: 800, y: 450, itemStyle: {color: '#4A6984'}}
                ],
                links: [
                    {source: 'A銀行\\n(保有原始個資)', target: 'CIB 中央 AI 大腦\\n(僅接收權重參數)'},
                    {source: 'B銀行\\n(保有原始個資)', target: 'CIB 中央 AI 大腦\\n(僅接收權重參數)'},
                    {source: 'C銀行\\n(保有原始個資)', target: 'CIB 中央 AI 大腦\\n(僅接收權重參數)'},
                    {source: 'D銀行\\n(保有原始個資)', target: 'CIB 中央 AI 大腦\\n(僅接收權重參數)'}
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