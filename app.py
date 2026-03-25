import streamlit as st
import random, json, os
from datetime import datetime
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY",""))

st.set_page_config(page_title="VEO3 AUTO SCALE SYSTEM", layout="wide")
st.title("🔥 VEO3 AUTO SCALE SYSTEM")

DATA_FILE = "data.json"
TREND_FILE = "trends.json"

# ================= FILE =================
def load_json(path, default):
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

# ================= HOOK ENGINE =================
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
        emotion=random.choice(["nghiện","mê","bất ngờ"])
    )

def get_best_hook():
    data = load_json(DATA_FILE, [])
    if data:
        best = sorted(data, key=lambda x: x["views"], reverse=True)
        return best[0]["hook"]
    return None

def hook_score(h):
    score = 0
    if "Ủa" in h: score += 2
    if "ai cũng" in h: score += 3
    if "luôn" in h: score += 2
    return score

def get_smart_hook():
    hooks = load_json(TREND_FILE, [])
    best = get_best_hook()

    pool = hooks + [ai_hook()]
    if best: pool.append(best)

    pool = sorted(pool, key=lambda x: hook_score(x), reverse=True)
    return pool[0]

# ================= STORY =================
def build_story(hook):
    return [
        ("0-3s","Close-up face",hook),
        ("3-6s","Macro product","Ủa có sẵn hết luôn hả?!"),
        ("6-10s","Use product","Tiện ghê luôn á"),
        ("10-15s","Lifestyle","Đi đâu cũng không cần mang dây"),
        ("15-20s","CTA","Mua cái này là đúng rồi")
    ]

# ================= PROMPT =================
def build_prompt(story):
    return f"""
MASTER LOCK
IDENTITY LOCK
PRODUCT LOCK
CONTINUITY LOCK

CAMERA + ACTION:
{story}

DIALOGUE:
Auto from storyboard

NEGATIVE:
No text overlay, no UI, no distortion
"""

# ================= IMAGE =================
def generate_image(prompt):
    if not client.api_key:
        return None
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1792"
    )
    return result.data[0].url

# ================= CAPTION =================
def caption():
    return random.choice([
        "Mua vì tò mò mà giờ nghiện luôn 😭",
        "Ai hay quên đồ chắc chắn cần cái này",
        "Không nghĩ nó tiện tới vậy luôn á"
    ])

def hashtag():
    return " ".join(random.sample(
        ["#tiktokshop","#viral","#review","#fyp","#xuhuong","#gadgets"],5))

def post_time():
    return "10h30-12h | 19h-22h" if datetime.now().weekday()>=5 else "11h30-13h | 19h-21h30"

# ================= INPUT =================
st.sidebar.header("INPUT")

variants = st.sidebar.slider("A/B test",1,5,3)
scale_mode = st.sidebar.checkbox("🔥 AUTO SCALE MODE")

# ================= GENERATE =================
if st.sidebar.button("🚀 GENERATE"):

    best_hook = get_best_hook()

    if best_hook:
        st.success(f"🔥 Hook WIN: {best_hook}")

    for i in range(variants):

        st.markdown(f"## 🎬 VIDEO {i+1}")

        if scale_mode and best_hook:
            hook = best_hook
        else:
            hook = get_smart_hook()

        story = build_story(hook)

        st.markdown("### 🎬 STORYBOARD")
        for t,a,d in story:
            st.write(f"{t} | {a} | {d}")

        st.markdown("### 📜 PROMPT")
        st.code(build_prompt(story))

        st.markdown("### 🖼 IMAGE")
        for idx,(t,a,_) in enumerate(story):
            if st.button(f"Gen {i}-{idx}"):
                img = generate_image(a)
                if img:
                    st.image(img)

        st.markdown("### 💰 TIKTOK")
        st.code(f"""
Caption:
{caption()}

Hashtag:
{hashtag()}

Time:
{post_time()}
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
