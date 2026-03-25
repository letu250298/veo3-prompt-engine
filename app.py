import streamlit as st
import random, json, os
from datetime import datetime
import pandas as pd
import openai

# ================= CONFIG =================
openai.api_key = st.secrets.get("OPENAI_API_KEY","")

DATA_FILE = "data.json"
TREND_FILE = "trends.json"

st.set_page_config(page_title="VEO3 FINAL SYSTEM", layout="wide")
st.title("🔥 VEO3 FINAL SYSTEM (ALL-IN-ONE)")

# ================= FILE =================
def load_json(path, default):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

# ================= INPUT =================
st.sidebar.markdown("## 📸 INPUT")

character = st.sidebar.file_uploader("Nhân vật", type=["png","jpg","jpeg"])
product = st.sidebar.file_uploader("Sản phẩm", type=["png","jpg","jpeg"])

if character:
    st.sidebar.image(character)

if product:
    st.sidebar.image(product)

duration = st.sidebar.selectbox("Duration",["8s","16s","24s"])
variants = st.sidebar.slider("A/B test",1,5,3)
scale_mode = st.sidebar.checkbox("🔥 AUTO SCALE")

# ================= HOOK =================
def ai_hook():
    patterns = [
        "Ủa cái này {insight} vậy luôn á?",
        "Không nghĩ nó lại {insight}",
        "Ai cũng đang xài cái này luôn",
        "Lướt TikTok thấy cái này hoài luôn",
        "Dùng thử mà {emotion} luôn"
    ]
    return random.choice(patterns).format(
        insight=random.choice(["tiện","xịn","đáng tiền"]),
        emotion=random.choice(["nghiện","mê"])
    )

def get_best_hook():
    data = load_json(DATA_FILE, [])
    if data:
        return sorted(data, key=lambda x:x["views"], reverse=True)[0]["hook"]
    return None

def get_hook():
    hooks = load_json(TREND_FILE, [])
    best = get_best_hook()
    pool = hooks + [ai_hook()]
    if best: pool.append(best)
    return random.choice(pool)

# ================= STORY =================
def build_story(hook, duration):

    if duration == "8s":
        return [
            ("0-2s","Close-up face",hook),
            ("2-5s","Macro product","Ủa có sẵn hết luôn hả?!"),
            ("5-8s","Plug phone","Thôi xong khỏi mang dây luôn")
        ]

    return [
        ("0-3s","Close-up",hook),
        ("3-6s","Macro product","Ủa tích hợp hết luôn hả?!"),
        ("6-10s","Use","Tiện ghê luôn"),
        ("10-15s","Lifestyle","Không cần mang dây"),
        ("15-20s","CTA","Mua cái này là đúng rồi")
    ]

# ================= PROMPT =================
def build_prompt(story):

    ref = ""
    if character:
        ref += "Use provided character reference image.\n"
    if product:
        ref += "Use provided product reference image.\n"

    return f"""
MASTER LOCK:
Mode: Image-to-Video using provided reference images only.
{ref}

IDENTITY LOCK:
Character must remain identical.

PRODUCT LOCK:
Product must remain identical.

CONTINUITY LOCK:
Maintain same scene.

CAMERA + ACTION:
{story}

DIALOGUE:
Exact from storyboard

NEGATIVE:
No text, no UI, no distortion
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

def img_prompt(action):
    return f"ultra realistic, {action}, soft light, 9:16, no text"

# ================= CONTENT =================
def caption():
    return random.choice([
        "Mua vì tò mò mà nghiện luôn 😭",
        "Ai hay quên đồ phải mua",
        "Không nghĩ nó tiện vậy luôn"
    ])

def hashtag():
    return " ".join(random.sample(
        ["#tiktokshop","#viral","#review","#fyp","#xuhuong"],5))

def time_post():
    return "19h-22h"

# ================= GENERATE =================
if st.sidebar.button("🚀 GENERATE"):

    best = get_best_hook()
    if best:
        st.success(f"🔥 Hook win: {best}")

    for i in range(variants):

        st.markdown(f"## 🎬 VIDEO {i+1}")

        hook = best if scale_mode and best else get_hook()

        story = build_story(hook, duration)

        st.markdown("### 🎬 STORYBOARD")
        for t,a,d in story:
            st.write(f"{t} | {a} | {d}")

        st.markdown("### 📜 PROMPT")
        st.code(build_prompt(story))

        st.markdown("### 🖼 IMAGE")
        for idx,(t,a,_) in enumerate(story):
            if st.button(f"Gen {i}-{idx}"):
                img = generate_image(img_prompt(a))
                if img:
                    st.image(img)

        st.markdown("### 💰 CONTENT")
        st.code(f"""
Caption: {caption()}
Hashtag: {hashtag()}
Time: {time_post()}
""")

# ================= TRACK =================
st.markdown("---")
st.markdown("## 📊 TRACK")

vid = st.text_input("Video ID")
hook_used = st.text_input("Hook")
views = st.number_input("Views",0)

if st.button("SAVE"):
    data = load_json(DATA_FILE, [])
    data.append({"video_id":vid,"hook":hook_used,"views":views})
    save_json(DATA_FILE,data)
    st.success("Saved!")

# ================= DASHBOARD =================
data = load_json(DATA_FILE, [])
if data:
    df = pd.DataFrame(data)
    st.dataframe(df)
    st.bar_chart(df.groupby("hook")["views"].mean())

# ================= TREND =================
st.markdown("## 🔥 ADD TREND")

new_hook = st.text_input("Hook mới")

if st.button("ADD"):
    data = load_json(TREND_FILE, [])
    data.append(new_hook)
    save_json(TREND_FILE,data)
    st.success("Added!")
