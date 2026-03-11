import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# --- 網頁基本設定 ---
st.set_page_config(page_title="金融犯罪情報中心", layout="wide")

# --- 模擬資料庫 ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        '帳戶代碼': ['ACCT_8839_A1', 'ACCT_3345_B2', 'ACCT_5512_C3', 'ACCT_1024_D4', 'ACCT_9921_E5'],
        '所屬機構': ['A銀行', 'B銀行', 'A銀行', 'C銀行', 'B銀行'],
        '近2日交易筆數': [45, 52, 12, 3, 8],
        '近2日轉入總額': [2500000, 3200000, 50000, 15000, 12000],
        '近2日轉出總額': [2495000, 3190000, 45000, 10000, 8000],
        '當前餘額': [5000, 10000, 25000, 55000, 150000],
        '風險指數': [98, 95, 45, 12, 8],
        '系統判定': ['極高風險_建議阻斷', '極高風險_建議阻斷', '中度風險_持續監控', '正常交易', '正常交易']
    })

df = load_data()

# --- 側邊欄：系統導覽 ---
st.sidebar.title("金融犯罪情報中心")
st.sidebar.caption("國家級異常資金流分析核心")
st.sidebar.markdown("---")
page = st.sidebar.radio("系統功能模組", [
    "戰情總覽與處置矩陣", 
    "跨機構資料匯入", 
    "案件深度調查",
    "跨機構聯邦學習架構 (願景)"
])
st.sidebar.markdown("---")
st.sidebar.write("**登入身分:** 系統管理員")
st.sidebar.write("**核心演算法:** XGBoost")
st.sidebar.write("**觀測視窗:** 2 日區塊")
st.sidebar.markdown("---")
st.sidebar.info("本系統落實資料極簡主義，僅接收去識別化交易特徵，符合隱私保護規範。")

# ==========================================
# 頁面 1：戰情總覽與處置矩陣
# ==========================================
if page == "戰情總覽與處置矩陣":
    st.title("戰情總覽與風險處置矩陣")
    st.markdown("即時監控跨機構交易特徵，並依據 AI 風險指數提供分級處置建議，兼顧風險攔截與正常顧客體驗。")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="今日掃描交易總筆數", value="159,543", delta="12% 增長")
    col2.metric(label="觸發警示帳戶數", value="2", delta="高風險名單", delta_color="inverse")
    col3.metric(label="預估攔截財損 TWD", value="5,700,000", delta="攔阻率 93.18%")
    col4.metric(label="系統誤報率 FPR", value="0.24%", delta="極低干擾", delta_color="normal")
    
    st.markdown("### 自動化風險分級處置準則")
    st.table(pd.DataFrame({
        '風險區間': ['> 90分 (極高風險)', '70 - 89分 (中高風險)', '< 70分 (低風險)'],
        '行為特徵吻合度': ['高度吻合「處置-多層化-整合」完整腳本', '具備異常資金突增，但尚未出現極速移轉', '行為落於常態分布範圍內'],
        '系統自動處置建議': ['🔴 立即觸發 API 阻斷網銀與非約轉功能', '🟡 觸發加強驗證 (OTP/視訊) 或背景限制', '🟢 寫入背景監控日誌，無須干擾客戶']
    }))

    st.markdown("### 高風險待處理清單")
    high_risk_df = df[df['風險指數'] > 80]
    st.dataframe(high_risk_df, use_container_width=True, hide_index=True)

# ==========================================
# 頁面 2：跨機構資料匯入
# ==========================================
elif page == "跨機構資料匯入":
    st.title("跨機構資料匯入與特徵萃取")
    st.markdown("模擬接收協力機構回傳之基礎交易紀錄，並啟動行為特徵矩陣轉換。")
    
    st.file_uploader("匯入交易紀錄 CSV 檔", type=['csv', 'xlsx'])
    
    if st.button("啟動 AI 特徵運算與風險評估", type="primary"):
        progress_text = "連線 API 接收資料中..."
        my_bar = st.progress(0, text=progress_text)
        time.sleep(1)
        my_bar.progress(30, text="資料合規驗證完成 (確認無隱私個資)")
        time.sleep(1)
        my_bar.progress(60, text="建立時間區塊與行為群組...")
        time.sleep(1)
        my_bar.progress(90, text="萃取 24 項行為特徵矩陣...")
        time.sleep(1)
        my_bar.progress(100, text="XGBoost 模型預測完成")
        st.success("批次資料分析完成，請至戰情總覽檢視高風險節點。")

# ==========================================
# 頁面 3：案件深度調查
# ==========================================
elif page == "案件深度調查":
    st.title("案件深度調查")
    st.markdown("透過特徵歸因與時間軸重建犯罪腳本，並自動生成執法公文。")
    
    selected_account = st.selectbox("請選擇目標調查帳戶：", df['帳戶代碼'])
    account_info = df[df['帳戶代碼'] == selected_account].iloc[0]
    
    st.subheader(f"目標帳戶狀態：{selected_account}")
    col_a, col_b, col_c = st.columns(3)
    col_a.write(f"**所屬機構:** {account_info['所屬機構']}")
    col_b.write(f"**當前餘額:** {account_info['當前餘額']:,} TWD")
    col_c.write(f"**風險指數:** {account_info['風險指數']}")
    
    st.markdown("---")
    
    if account_info['風險指數'] > 80:
        tab1, tab2, tab3, tab4 = st.tabs(["資金流向知識圖譜", "特徵歸因分析 SHAP", "動態行為時間軸", "司法警示通報生成"])
        
        with tab1:
            st.markdown("資金節點關聯分析顯示該帳戶呈現典型之**「多進多出、快速分流」**特徵。")
            graph_html = f"""
            <!DOCTYPE html><html><head><script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script></head>
            <body style="margin:0; padding:0;"><div id="main" style="width: 100%; height: 450px;"></div>
            <script>
                var chart = echarts.init(document.getElementById('main'));
                chart.setOption({{
                    series: [{{
                        type: 'graph', layout: 'force', symbolSize: 60, roam: true,
                        label: {{ show: true, fontSize: 14, color: '#fff' }},
                        edgeSymbol: ['none', 'arrow'], edgeSymbolSize: [4, 10], force: {{ repulsion: 1000, edgeLength: 150 }},
                        data: [
                            {{name: '被害人 A\\n(匯入)', itemStyle: {{color: '#4A6984'}}}},
                            {{name: '被害人 B\\n(匯入)', itemStyle: {{color: '#4A6984'}}}},
                            {{name: '目標帳戶\\n{selected_account}', itemStyle: {{color: '#A03232'}}, symbolSize: 85}},
                            {{name: '中繼戶 C\\n(轉出)', itemStyle: {{color: '#D48A41'}}}},
                            {{name: '虛擬資產\\n交易所', itemStyle: {{color: '#526A54'}}}}
                        ],
                        links: [
                            {{source: '被害人 A\\n(匯入)', target: '目標帳戶\\n{selected_account}', label: {{show: true, formatter: '處置'}}}},
                            {{source: '被害人 B\\n(匯入)', target: '目標帳戶\\n{selected_account}', label: {{show: true, formatter: '處置'}}}},
                            {{source: '目標帳戶\\n{selected_account}', target: '中繼戶 C\\n(轉出)', label: {{show: true, formatter: '多層化'}}}},
                            {{source: '中繼戶 C\\n(轉出)', target: '虛擬資產\\n交易所', label: {{show: true, formatter: '整合'}}}}
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
            st.markdown("### ⏱️ 2 日觀測視窗內的犯罪倒數計時")
            st.markdown("藉由系統抓取的最短時間間隔，可發現犯罪集團受限於「洗錢時間壓力」，必須在極短時間內完成移轉。")
            now = datetime.now()
            st.info(f"**T=0 ({(now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')})**：被害人 A 匯入 1,000,000 元 (觸發處置階段)")
            st.warning(f"**T+12 分鐘 ({(now - timedelta(hours=1, minutes=48)).strftime('%H:%M')})**：被害人 B 匯入 1,500,000 元 (觸發高頻入金特徵)")
            st.error(f"**T+25 分鐘 ({(now - timedelta(hours=1, minutes=35)).strftime('%H:%M')})**：該帳戶透過網銀將 1,200,000 轉至中繼帳戶 (觸發多層化極速轉出特徵)")
            st.error(f"**T+45 分鐘 ({(now - timedelta(minutes=75)).strftime('%H:%M')})**：餘額降至 5,000 元 (觸發整合清空特徵，AI 風險指數達 98 分)")

        with tab4:
            st.markdown("### 📄 自動生成：司法調閱與警示通報公文")
            st.write("系統已根據 AI 判讀結果，自動帶入相關數據與法條，可直接複製提供給協力銀行。")
            
            official_doc = f"""發文機關：內政部警政署刑事警察局 (模擬)
受文者：{account_info['所屬機構']}
發文日期：中華民國 {datetime.now().year - 1911} 年 {datetime.now().month} 月 {datetime.now().day} 日

主旨：有關貴機構帳戶 {selected_account} 涉嫌假投資詐欺洗錢異常，建請即刻執行帳戶圈存與非約轉限制，請查照。

說明：
一、依據「國家級金融情報預警系統」動態行為分析，該帳戶近 2 日內資金呈極高風險（AI 評分：{account_info['風險指數']} 分）。
二、經查該帳戶行為軌跡符合「處置、多層化、整合」之洗錢特徵。其於 2 日內累計匯入 {account_info['近2日轉入總額']:,} 元，並於極短時間內密集轉出 {account_info['近2日轉出總額']:,} 元，致使當前餘額僅剩 {account_info['當前餘額']:,} 元。
三、為防止社會財損擴大，依據警示帳戶聯防機制，建請貴機構先行啟動阻斷機制，本局後續將由專責人員介入調閱偵辦。"""
            
            st.code(official_doc, language="markdown")

    else:
        st.success("行為腳本判定：未檢測出顯著之洗錢特徵。")

# ==========================================
# 頁面 4：跨機構聯邦學習架構
# ==========================================
elif page == "跨機構聯邦學習架構 (願景)":
    st.title("🌐 跨機構聯邦學習拓撲 (Federated Learning)")
    st.markdown("""
    **突破「數據孤島」的終極解方**：
    未來 Phase 3 將推動聯邦學習。各銀行的**客戶個資與交易明細「絕對不出戶」**，僅將 AI 學習到的「行為特徵權重（模型參數）」上傳至情報中心。情報中心統整後再下派更新給全體銀行，實現**「一家發現，全體免疫」**的國家級聯防網路。
    """)
    
    fed_html = """
    <!DOCTYPE html><html><head><script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script></head>
    <body style="margin:0; padding:0;"><div id="main" style="width: 100%; height: 500px;"></div>
    <script>
        var chart = echarts.init(document.getElementById('main'));
        chart.setOption({
            backgroundColor: '#0E1117',
            title: { text: '模型參數動態交換模擬', textStyle: {color: '#fff'} },
            series: [{
                type: 'graph', layout: 'none', symbolSize: 70,
                label: { show: true, color: '#fff', fontSize: 14, position: 'bottom' },
                data: [
                    {name: '情報中心 AI大腦\\n(參數聚合)', x: 500, y: 300, itemStyle: {color: '#A03232'}, symbolSize: 100},
                    {name: 'A銀行\\n(本地訓練)', x: 200, y: 150, itemStyle: {color: '#4A6984'}},
                    {name: 'B銀行\\n(本地訓練)', x: 800, y: 150, itemStyle: {color: '#4A6984'}},
                    {name: 'C銀行\\n(本地訓練)', x: 200, y: 450, itemStyle: {color: '#4A6984'}},
                    {name: 'D銀行\\n(本地訓練)', x: 800, y: 450, itemStyle: {color: '#4A6984'}}
                ],
                links: [
                    {source: 'A銀行\\n(本地訓練)', target: '情報中心 AI大腦\\n(參數聚合)'},
                    {source: 'B銀行\\n(本地訓練)', target: '情報中心 AI大腦\\n(參數聚合)'},
                    {source: 'C銀行\\n(本地訓練)', target: '情報中心 AI大腦\\n(參數聚合)'},
                    {source: 'D銀行\\n(本地訓練)', target: '情報中心 AI大腦\\n(參數聚合)'}
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
    components.html(fed_html, height=520)