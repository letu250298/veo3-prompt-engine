import streamlit as st
import random, json, os
from datetime import datetime
import pandas as pd

# ================= CONFIG =================
DATA_FILE = "data.json"
TREND_FILE = "trends.json"

st.set_page_config(page_title="VEO3 MONEY SYSTEM", layout="wide")
st.title("🔥 VEO3 MONEY SYSTEM (Trend + AB Test + Dashboard)")

# ================= UTIL =================
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================= TREND ENGINE =================
default_hooks = [
    "Ủa… sao giờ ai cũng xài cái này vậy?",
    "Lướt TikTok thấy cái này hoài luôn",
    "Không nghĩ là nó tiện vậy luôn á",
    "Ai cũng mua cái này luôn á trời",
    "Review thật, không PR nha 😭"
]

def get_trend_hooks():
    data = load_json(TREND_FILE, [])
    return data if data else default_hooks

# ================= TRACKING =================
def save_result(video_id, hook, views):
    data = load_json(DATA_FILE, [])
    data.append({
        "video_id": video_id,
        "hook": hook,
        "views": views,
        "date": str(datetime.now())
    })
    save_json(DATA_FILE, data)

def get_data():
    return load_json(DATA_FILE, [])

# ================= AB TEST =================
def generate_hooks(n=5):
    hooks = get_trend_hooks()
    return random.sample(hooks, min(n, len(hooks)))

# ================= STORYBOARD =================
def build_story(hook):
    return [
        ("0-3s", "Close-up face", hook),
        ("3-6s", "Macro product", "Ủa có sẵn hết luôn hả?!"),
        ("6-10s", "Use product", "Tiện ghê luôn á"),
        ("10-15s", "Lifestyle", "Đi đâu cũng không cần mang dây"),
        ("15-20s", "CTA", "Mua cái này là đúng rồi")
    ]

# ================= PROMPT =================
def build_prompt(story):
    return f"""
MASTER LOCK
IDENTITY LOCK
PRODUCT LOCK
CONTINUITY LOCK

SCENES:
{story}

NEGATIVE: no text, no UI, no distortion
"""

# ================= UI =================

tab1, tab2, tab3 = st.tabs(["🎬 Generate", "📊 Dashboard", "🔥 Trend"])

# ===== TAB 1 GENERATE =====
with tab1:

    st.subheader("🎯 Generate Video Ideas")

    if st.button("🚀 Generate 5 Hooks (A/B test)"):

        hooks = generate_hooks()

        for i, hook in enumerate(hooks):

            st.markdown(f"### 🎬 Video {i+1}")
            story = build_story(hook)

            st.write("Storyboard:")
            for t,a,d in story:
                st.write(f"{t} | {a} | {d}")

            st.code(build_prompt(story))

# ===== TAB 2 DASHBOARD =====
with tab2:

    st.subheader("📊 Tracking")

    data = get_data()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)

        st.subheader("🏆 Best Hooks")
        best = df.groupby("hook")["views"].mean().sort_values(ascending=False)
        st.bar_chart(best)

    else:
        st.info("Chưa có dữ liệu")

    st.subheader("➕ Thêm dữ liệu video")

    video_id = st.text_input("Video ID")
    hook = st.text_input("Hook")
    views = st.number_input("Views", 0)

    if st.button("💾 Save"):
        save_result(video_id, hook, views)
        st.success("Saved!")

# ===== TAB 3 TREND =====
with tab3:

    st.subheader("🔥 Update Trend Hooks")

    st.write("👉 Paste hook từ TikTok Creative Center")

    new_hook = st.text_input("Hook mới")

    if st.button("➕ Add Hook"):
        data = load_json(TREND_FILE, [])
        data.append(new_hook)
        save_json(TREND_FILE, data)
        st.success("Added!")

    st.write("Current hooks:")
    st.json(load_json(TREND_FILE, default_hooks))
