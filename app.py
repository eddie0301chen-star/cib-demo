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
    st.session_state.page = "戰情總覽與防阻成效"
if 'target_account' not in st.session_state:
    st.session_state.target_account = "ACCT_8839_A1"
if 'model_aggregated' not in st.session_state:
    st.session_state.model_aggregated = False

def set_page():
    st.session_state.page = st.session_state.sidebar_radio

def jump_to_investigate(account_id):
    st.session_state.target_account = account_id
    st.session_state.page = "帳戶與群聚網絡深度調查"

# --- 模擬資料庫 ---
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
st.sidebar.caption("跨機構異常資金流聯防系統")
st.sidebar.markdown("---")

# 重新排序模組：2與4合併至最後
pages = ["戰情總覽與防阻成效", "帳戶與群聚網絡深度調查", "跨機構模型協作與測試中心"]
st.sidebar.radio("系統功能模組", pages, index=pages.index(st.session_state.page), key="sidebar_radio", on_change=set_page)

st.sidebar.markdown("---")
st.sidebar.write("**使用者單位:** 刑事警察局 情報科")
st.sidebar.write("**系統狀態:** 正常連線")
st.sidebar.write("**觀測視窗:** 2 日區塊特徵")

# ==========================================
# 頁面 1：戰情總覽與防阻成效
# ==========================================
if st.session_state.page == "戰情總覽與防阻成效":
    st.title("戰情總覽與防阻成效")
    st.markdown("依據洗錢前置行為與資金突發特徵，進行風險分級與派發處置。")
    
    st.subheader("當日系統運作指標")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="當日解析特徵筆數", value="159,543", delta="12% 增量")
    col2.metric(label="列管觀察帳戶", value="4", delta="需持續查核")
    col3.metric(label="觸發處置帳戶", value="4", delta="建議立即圈存", delta_color="inverse")
    col4.metric(label="系統誤報率 (FPR)", value="0.24%", delta="符合系統基準", delta_color="normal")
    
    st.markdown("---")
    
    st.subheader("本月防堵成效統計")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="本月通報處置帳戶", value="128 戶", delta="較上月 +15%")
    col_b.metric(label="本月保全不法資金", value="1.5 億 TWD", delta="實質攔阻金額")
    col_c.metric(label="年度預估攔阻總額", value="18.5 億 TWD", delta="依當前預警模型推算")
    
    st.markdown("---")
    
    colA, colB = st.columns(2)
    with colA:
        st.subheader("列管中：高風險觀察清單")
        st.caption("具備前置異常特徵，尚未發生大額匯轉。")
        monitor_df = df[df['案件狀態'].str.contains('🟡')].reset_index(drop=True)
        for index, row in monitor_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([4, 3, 3])
                c1.write(f"**{row['帳戶代碼']}**\n({row['所屬機構']})")
                c2.write(f"風險評分: {row['風險指數']}")
                c3.button("啟動調查", key=f"btn_y_{index}", on_click=jump_to_investigate, args=(row['帳戶代碼'],), use_container_width=True)
                st.divider()

    with colB:
        st.subheader("待處置：觸發大額匯轉清單")
        st.caption("列管帳戶已接收大額資金，呈洗錢移轉特徵。")
        action_df = df[df['案件狀態'].str.contains('🔴')].reset_index(drop=True)
        for index, row in action_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([4, 3, 3])
                c1.write(f"**{row['帳戶代碼']}**\n({row['所屬機構']})")
                c2.write(f"風險評分: {row['風險指數']}")
                c3.button("執行處置", key=f"btn_r_{index}", on_click=jump_to_investigate, args=(row['帳戶代碼'],), use_container_width=True)
                st.divider()

# ==========================================
# 頁面 2：帳戶與群聚網絡深度調查 (全新升級)
# ==========================================
elif st.session_state.page == "帳戶與群聚網絡深度調查":
    st.title("帳戶與群聚網絡深度調查")
    
    account_list = df['帳戶代碼'].tolist()
    default_idx = account_list.index(st.session_state.target_account) if st.session_state.target_account in account_list else 0
    selected_account = st.selectbox("標的帳戶查詢：", account_list, index=default_idx)
    account_info = df[df['帳戶代碼'] == selected_account].iloc[0]
    
    is_red = '🔴' in account_info['案件狀態']
    
    col_a, col_b, col_c = st.columns(3)
    col_a.write(f"**所屬機構:** {account_info['所屬機構']}")
    col_b.write(f"**帳戶餘額:** {account_info['當前餘額']:,} TWD")
    col_c.write(f"**系統判定狀態:** {account_info['案件狀態']}")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["關聯圖譜 (資金與數位足跡)", "群聚風險與擴線建議", "特徵歸因分析", "聯防通報作業"])
    
    with tab1:
        st.markdown("分析標的帳戶之資金流向拓撲，並疊加裝置指紋/IP等數位足跡進行交叉比對。")
        # 實務視覺化：實線為金流，虛線為共用IP/設備
        nodes = [
            f"{{name: '上游來源 (異常匯入)', itemStyle: {{color: '#4A6984'}} }}",
            f"{{name: '標的帳戶\\n{selected_account}', itemStyle: {{color: '#A03232'}}, symbolSize: 70 }}",
            f"{{name: '關聯帳戶 X\\n(B銀行)', itemStyle: {{color: '#D48A41'}} }}",
            f"{{name: '關聯帳戶 Y\\n(C銀行)', itemStyle: {{color: '#D48A41'}} }}"
        ]
        links = [
            f"{{source: '上游來源 (異常匯入)', target: '標的帳戶\\n{selected_account}', label: {{show: true, formatter: '資金匯入'}}, lineStyle: {{type: 'solid'}} }}",
            f"{{source: '標的帳戶\\n{selected_account}', target: '關聯帳戶 X\\n(B銀行)', label: {{show: true, formatter: '共用登入 IP'}}, lineStyle: {{type: 'dashed', color: '#ff9900'}} }}",
            f"{{source: '標的帳戶\\n{selected_account}', target: '關聯帳戶 Y\\n(C銀行)', label: {{show: true, formatter: '同設備 Device ID'}}, lineStyle: {{type: 'dashed', color: '#ff9900'}} }}"
        ]
        if is_red:
            nodes.append(f"{{name: '下游分流戶 Z\\n(A銀行)', itemStyle: {{color: '#526A54'}} }}")
            links.append(f"{{source: '標的帳戶\\n{selected_account}', target: '下游分流戶 Z\\n(A銀行)', label: {{show: true, formatter: '大額資金移轉'}}, lineStyle: {{type: 'solid'}} }}")

        graph_html = f"""
        <!DOCTYPE html><html><head><script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script></head>
        <body style="margin:0; padding:0;"><div id="main" style="width: 100%; height: 400px;"></div>
        <script>
            var chart = echarts.init(document.getElementById('main'));
            chart.setOption({{
                legend: {{ data: ['資金流向 (實線)', '數位足跡關聯 (虛線)'] }},
                series: [{{
                    type: 'graph', layout: 'force', symbolSize: 55, roam: true,
                    label: {{ show: true, fontSize: 12, color: '#fff' }},
                    edgeSymbol: ['none', 'arrow'], edgeSymbolSize: [4, 8], force: {{ repulsion: 800, edgeLength: 150 }},
                    data: [{','.join(nodes)}],
                    links: [{','.join(links)}]
                }}]
            }});
        </script></body></html>
        """
        components.html(graph_html, height=420)
        st.caption("圖例說明：實線代表實質資金流動；虛線代表未發生交易，但具備共用數位足跡（IP/裝置）之高度嫌疑帳戶。")

    with tab2:
        st.markdown("依據網路圖譜關聯度，系統自動提取具備高度共犯嫌疑之擴線清單。")
        st.table(pd.DataFrame({
            '關聯帳戶代碼': ['ACCT_9882_B2 (關聯帳戶 X)', 'ACCT_1002_C3 (關聯帳戶 Y)', 'ACCT_4431_A1 (下游分流戶 Z)'],
            '所屬機構': ['B銀行', 'C銀行', 'A銀行'],
            '關聯原因判定': ['與標的帳戶共用同一境外 IP (104.28.x.x) 登入網銀', '與標的帳戶具備相同行動裝置指紋 (Device ID)', '接收標的帳戶 80% 以上之匯出資金'],
            '處置建議': ['建議併案列管，進行加強查核 (EDD)', '建議併案列管，進行加強查核 (EDD)', '建議同步執行預防性圈存']
        }))

    with tab3:
        st.markdown("標的帳戶決策權重解析 (基於行為特徵模型)：")
        shap_data = pd.DataFrame({
            '行為特徵變數': ['單筆金額標準差異常', '入金時間密集度', '移轉時間間隔(秒)', '網銀登入頻率異常', '餘額清空指標'],
            '權重影響係數': [0.88, 0.75, 0.68, 0.52, 0.41] if is_red else [0.25, 0.12, 0.78, 0.65, 0.15]
        }).sort_values(by='權重影響係數', ascending=True)
        st.bar_chart(shap_data.set_index('行為特徵變數'), color="#6c757d")

    with tab4:
        st.markdown("產出批次聯防通報公文，針對標的帳戶與關聯群聚帳戶進行同步處置。")
        official_doc = f"""發文機關：內政部警政署刑事警察局
受文者：{account_info['所屬機構']} 及相關金融機構 法遵與風控部門
主旨：有關帳戶 {selected_account} 及其數位足跡關聯帳戶，涉及洗錢異常行為，建請依防詐聯防機制辦理，請查照。
說明：
一、本局資訊系統偵測帳戶 {selected_account} 具備顯著異常資金與操作特徵。
二、經系統擴線分析，發現另有帳戶 (詳見系統附表) 與該標的帳戶存在共用登入 IP 與裝置指紋之異常關聯，研判為同一犯罪群聚操作。
三、為阻斷不法金流，建請貴機構對上述清單帳戶依風險等級執行「預防性圈存」或「加強客戶盡職審查 (EDD)」，本局將接續辦理相關偵查作為。"""
        st.code(official_doc, language="markdown")

# ==========================================
# 頁面 3：跨機構模型協作與測試中心 (模組2與4整合)
# ==========================================
elif st.session_state.page == "跨機構模型協作與測試中心":
    st.title("跨機構模型協作與測試中心")
    st.markdown("透過聯邦學習架構，接收各機構本地端訓練之模型參數，進行全域聚合與效能驗證，解決跨機構資料隱私限制。")
    
    st.subheader("1. 模型參數接收與聚合 (Federated Aggregation)")
    st.markdown("接收各金融機構於本地端依據最新異常樣態所訓練之權重參數，進行特徵空間聚合，生成全局模型。")
    
    col_x, col_y, col_z = st.columns(3)
    col_x.info("📥 已接收: A銀行 權重參數檔 (.pt)\n\n包含特徵: 虛擬貨幣快進快出")
    col_y.info("📥 已接收: B銀行 權重參數檔 (.pt)\n\n包含特徵: 第三方支付異常")
    col_z.info("📥 已接收: C銀行 權重參數檔 (.pt)\n\n包含特徵: 跨國 IP 跳轉異常")
    
    if st.button("執行全域模型參數聚合", type="primary"):
        with st.spinner("執行參數聚合 (Federated Averaging) 作業中..."):
            time.sleep(2)
        st.session_state.model_aggregated = True
        st.success("作業完成：已成功產出並註冊 [全局聚合聯合防禦模型 v3.0]。")

    st.markdown("---")
    
    st.subheader("2. 預警模型版本庫 (Model Registry)")
    model_options = [
        "[當前上線] XGBoost 假投資特化版_v2.1",
        "[歷史基準] RandomForest 基礎洗錢防制版_v1.0"
    ]
    if st.session_state.model_aggregated:
        model_options.insert(0, "[最新聚合] 全局聯合防禦模型_v3.0 (待驗證)")
        
    selected_model = st.selectbox("請選擇系統掛載之預測模型：", model_options)

    st.markdown("---")
    
    st.subheader("3. 模型效能驗證與測試 (Validation & Testing)")
    tab_api, tab_upload = st.tabs(["API 串接驗證", "歷史特徵批次驗證"])
    
    with tab_api:
        st.markdown("驗證指定模型處理即時連線資料流之效能與反應時間。")
        st.text_input("連線通道 (API Endpoint)", value="https://api.cib.gov.tw/v1/model-test/stream", disabled=True)
        if st.button("執行 API 模擬驗證"):
            with st.spinner(f"掛載 {selected_model.split(' ')[0]} 進行資料流解析..."):
                time.sleep(1.5)
            st.success("驗證通過：資料流處理延遲 < 50ms，記憶體占用正常。")

    with tab_upload:
        st.markdown("匯入去識別化之歷史交易特徵集，驗證模型預測準確率 (Precision/Recall)。")
        st.file_uploader("匯入測試特徵集 (CSV 格式)", type=['csv'])
        if st.button("執行批次效能驗證"):
            with st.spinner("計算模型混淆矩陣與效能指標..."):
                time.sleep(2)
            report_col1, report_col2, report_col3 = st.columns(3)
            report_col1.metric("模型精確率 (Precision)", "91.2%")
            report_col2.metric("模型召回率 (Recall)", "88.5%")
            report_col3.metric("F1-Score", "89.8%")
            st.success("驗證完成，該模型效能優於基準，可評估排程上線。")