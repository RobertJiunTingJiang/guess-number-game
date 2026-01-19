import streamlit as st
import random
from supabase import create_client, Client
import time

# --- Supabase 設定 ---
SUPABASE_URL = "https://tavstphloajcmrfkgzkv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRhdnN0cGhsb2FqY21yZmtnemt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5MzcxNzUsImV4cCI6MjA4MzUxMzE3NX0.GG-f63-TTGbWapOQrKLxjQt3axCnMOcqUIp_24eHwLg"

# 在舊版 supabase-py 中，ClientOptions 可能不在根目錄或命名不同
# 我們直接建立 client，逾時問題我們透過重試機制來彌補
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 頁面設定 ---
icon_url = "https://raw.githubusercontent.com/RobertJiunTingJiang/guess-number-game/main/app_icon.png"
st.set_page_config(page_title="猜數字遊戲 Pro", page_icon=icon_url)

# PWA 標籤注入
st.markdown(
    """
    <link rel="manifest" href="https://raw.githubusercontent.com/RobertJiunTingJiang/guess-number-game/main/manifest.json?v=2">
    <meta name="theme-color" content="#4A90E2">
    <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/RobertJiunTingJiang/guess-number-game/main/app_icon.png">
    """,
    unsafe_allow_html=True
)

# --- 初始化 session_state ---
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 10)
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'data_sent' not in st.session_state:
    st.session_state.data_sent = False

def reset_game():
    st.session_state.target_number = random.randint(1, 10)
    st.session_state.count = 0
    st.session_state.message = ""
    st.session_state.game_over = False
    st.session_state.data_sent = False

st.title("🎯 猜數字遊戲 v1.11 (PWA 版)")

# 玩家資訊
player_name = st.text_input("請輸入你的大名：", value="匿名玩家", key="player_name_input")

st.divider()

# 遊戲說明
st.write(f"你好 **{player_name}**！我已經選好了一個 1-10 的數字。開始猜吧！")

# 數字輸入框
guess = st.number_input("輸入你的猜測：", min_value=1, max_value=100, step=1, key="guess_input", disabled=st.session_state.game_over)

# 猜測邏輯
if st.button("提交猜測") and not st.session_state.game_over:
    st.session_state.count += 1
    if guess < st.session_state.target_number:
        st.session_state.message = f"太小了！"
    elif guess > st.session_state.target_number:
        st.session_state.message = f"太大了！"
    else:
        st.session_state.message = f"🎉 恭喜 **{player_name}** 猜對了！正確答案是 {st.session_state.target_number}。"
        st.session_state.game_over = True

# 顯示訊息與寫入資料庫
if st.session_state.message:
    if "恭喜" in st.session_state.message:
        st.success(st.session_state.message)
        
        # 寫入 Supabase (確保只傳送一次)
        if not st.session_state.data_sent:
            status_placeholder = st.empty()
            with st.spinner("正在連線至排行伺服器..."):
                success = False
                for attempt in range(3):
                    try:
                        data = {
                            "player_name": player_name,
                            "attempts": st.session_state.count
                        }
                        supabase.table("py_scores_0120c").insert(data).execute()
                        success = True
                        st.session_state.data_sent = True
                        break
                    except Exception as e:
                        time.sleep(1.5)
                
                if success:
                    st.success(f"✅ 排行榜已更新！你名列其中囉！")
                else:
                    st.error("❌ 網路連線繁忙，暫時無法更新排行榜，請稍後再試。")
    else:
        st.warning(st.session_state.message)

# --- 排行榜顯示區 ---
st.divider()
st.subheader("🏆 全球排行榜 (前 10 名)")
try:
    # 抓取猜測次數最少的前 10 名
    res = supabase.table("py_scores_0120c").select("player_name, attempts, created_at").order("attempts", desc=False).limit(10).execute()
    if res.data:
        import pandas as pd
        df = pd.DataFrame(res.data)
        df.columns = ['玩家名稱', '猜測次數', '日期']
        st.dataframe(df, use_container_width=True)
    else:
        st.write("目前還沒有紀錄，快來搶下第一名！")
except Exception:
    st.write("暫時無法載入排行榜。")

# 顯示目前的猜測步數
st.info(f"📊 你目前的猜測次數：`{st.session_state.count}`")

# 操作按鈕
col1, col2 = st.columns(2)
with col1:
    if st.session_state.game_over:
        if st.button("再玩一局"):
            reset_game()
            st.experimental_rerun()
with col2:
    if st.button("重置目前遊戲"):
        reset_game()
        st.experimental_rerun()
