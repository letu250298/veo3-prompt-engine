import streamlit as st
import random, json, os
from datetime import datetime
import pandas as pd
import openai

openai.api_key = st.secrets.get("OPENAI_API_KEY","")

DATA_FILE = "data.json"
TREND_FILE = "trends.json"

st.set_page_config(layout="wide")
st.title("🎬 VEO AI STUDIO PRO")

# ================= FILE =================
def load_json(path, default):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

# ================= SIDEBAR =================
with st.sidebar:

    st.markdown("## 📥 INPUT")

    character = st.file_uploader("Character", type=["png","jpg"])
    product = st.file_uploader("Product", type=["png","jpg"])

    if character: st.image(character)
    if product: st.image(product)

    prompt_input = st.text_area("Custom Prompt")

    st.markdown("## ⚙️ SETTINGS")

    duration = st.selectbox("Duration",["8s","16s","24s"])
    variants = st.slider("Variants",1,5,3)
    scale_mode = st.checkbox("Auto Scale")

    generate = st.button("🚀 GENERATE")

# ================= HOOK =================
def ai_hook():
    return random.choice([
        "Ủa cái này là gì vậy?",
        "Ai cũng đang xài cái này luôn",
        "Lướt TikTok thấy cái này hoài",
        "Không nghĩ nó tiện vậy luôn"
    ])

def get_best_hook():
    data = load_json(DATA_FILE, [])
    if data:
        return sorted(data, key=lambda x:x["views"], reverse=True)[0]["hook"]
    return None

# ================= STORY =================
def build_story(hook):
    return [
        ("0-3s","Close-up",hook),
        ("3-6s","Product reveal","Ủa có sẵn hết luôn hả?!"),
        ("6-10s","Use","Tiện ghê luôn")
    ]

# ================= PROMPT =================
def build_prompt(story):

    ref = ""
    if character:
        ref += "Use provided character reference.\n"
    if product:
        ref += "Use provided product reference.\n"

    return f"""
MASTER LOCK
IDENTITY LOCK
PRODUCT LOCK
CONTINUITY LOCK

{ref}

SCENES:
{story}

NEGATIVE:
no text, no UI
"""

# ================= IMAGE =================
def generate_image(prompt):
    if not openai.api_key:
        return None
    res = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1792"
    )
    return res.data[0].url

# ================= CONTENT =================
def caption():
    return "Mua vì tò mò mà nghiện luôn 😭"

def hashtag():
    return "#tiktokshop #viral #fyp"

def time_post():
    return "19h-22h"

# ================= GENERATE =================
if generate:

    tabs = st.tabs([
        "📜 Script",
        "🎬 Storyboard",
        "🎥 Prompt",
        "🖼 Image",
        "💰 Content",
        "📊 Analytics"
    ])

    all_data = []

    for i in range(variants):

        hook = get_best_hook() if scale_mode else ai_hook()
        story = build_story(hook)

        all_data.append((hook, story))

    # ===== SCRIPT =====
    with tabs[0]:
        for i,(hook,story) in enumerate(all_data):
            st.markdown(f"### Version {i+1}")
            st.write(hook)

    # ===== STORYBOARD =====
    with tabs[1]:
        for i,(hook,story) in enumerate(all_data):
            st.markdown(f"### Version {i+1}")
            for t,a,d in story:
                st.write(f"{t} | {d}")

    # ===== PROMPT =====
    with tabs[2]:
        for i,(hook,story) in enumerate(all_data):
            st.code(build_prompt(story))

    # ===== IMAGE =====
    with tabs[3]:
        for i,(hook,story) in enumerate(all_data):
            for idx,(t,a,_) in enumerate(story):
                if st.button(f"Gen {i}-{idx}"):
                    img = generate_image(a)
                    if img:
                        st.image(img)

    # ===== CONTENT =====
    with tabs[4]:
        st.code(f"""
Caption: {caption()}
Hashtag: {hashtag()}
Time: {time_post()}
""")

    # ===== ANALYTICS =====
    with tabs[5]:
        data = load_json(DATA_FILE, [])
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.groupby("hook")["views"].mean())

# ================= TRACK =================
st.markdown("---")
st.markdown("## 📊 Track")

vid = st.text_input("Video ID")
hook_used = st.text_input("Hook used")
views = st.number_input("Views",0)

if st.button("Save"):
    data = load_json(DATA_FILE, [])
    data.append({"video_id":vid,"hook":hook_used,"views":views})
    save_json(DATA_FILE,data)
    st.success("Saved")
