import streamlit as st
import random, json, os
from datetime import datetime
import pandas as pd
import openai

openai.api_key = st.secrets.get("OPENAI_API_KEY","")

st.set_page_config(page_title="VEO3 ULTRA SYSTEM", layout="wide")
st.title("🔥 VEO3 ULTRA SYSTEM (QUALITY + SCALE + AI)")

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
        insight=random.choice(["tiện","xịn","đáng tiền","nhỏ mà có võ"]),
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

# ================= STORYBOARD =================
def build_story(hook, duration):

    if duration == "8s":
        return [
            ("0-2s","Close-up face, confused expression",hook),
            ("2-5s","Macro product, cable reveal slowly","Ủa có sẵn hết luôn hả?!"),
            ("5-8s","Plug phone, screen lights up","Thôi xong khỏi mang dây luôn.")
        ]

    return [
        ("0-3s","Close-up face reaction",hook),
        ("3-6s","Macro product detail","Ủa nó tích hợp hết luôn hả?!"),
        ("6-10s","Use product","Tiện ghê luôn á"),
        ("10-15s","Lifestyle usage","Đi đâu cũng không cần mang dây"),
        ("15-20s","CTA shot","Mua cái này là đúng rồi")
    ]

# ================= PROMPT =================
def build_prompt(story):

    return f"""
MASTER LOCK:
Mode: Image-to-Video using provided reference images only.

IDENTITY LOCK:
Character must remain identical to reference image.
Do NOT change face, hair, body.

PRODUCT LOCK:
Product must remain identical.
No redesign, no color change.

CONTINUITY LOCK:
Maintain same character, product, lighting.

CAMERA + ACTION:
{story}

DIALOGUE:
Use exact dialogue from storyboard.

NEGATIVE:
NO TEXT OVERLAY
NO SUBTITLES
NO UI
NO EXTRA OBJECTS
NO DISTORTION
"""

# ================= IMAGE =================
def generate_image(prompt):
    if not openai.api_key:
        return None

    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1792"
    )

    return response.data[0].url

def build_image_prompt(action):
    return f"""
Ultra realistic product shot,
{action},
clean background,
soft lighting,
9:16 vertical,
TikTok style,
no text,
sharp focus
"""

# ================= CAPTION =================
def caption():
    return random.choice([
        "Mua vì tò mò mà giờ nghiện luôn 😭",
        "Ai hay quên đồ chắc chắn cần cái này",
        "Không nghĩ nó tiện tới vậy luôn á",
        "Đi đâu cũng mang cái này là đủ"
    ])

def hashtag():
    return " ".join(random.sample(
        ["#tiktokshop","#viral","#review","#fyp","#xuhuong","#gadgets","#musthave"],5))

def post_time():
    return "10h30-12h | 19h-22h" if datetime.now().weekday()>=5 else "11h30-13h | 19h-21h30"

# ================= UI =================
st.sidebar.header("CONTROL")

duration = st.sidebar.selectbox("Duration",["8s","16s","24s"])
variants = st.sidebar.slider("A/B test",1,5,3)
scale_mode = st.sidebar.checkbox("🔥 AUTO SCALE (reuse hook win)")

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

        story = build_story(hook, duration)

        # STORYBOARD
        st.markdown("### 🎬 STORYBOARD")
        for t,a,d in story:
            st.write(f"{t} | {a} | {d}")

        # PROMPT
        st.markdown("### 📜 VEO PROMPT")
        prompt = build_prompt(story)
        st.code(prompt)

        # IMAGE
        st.markdown("### 🖼 SCENE IMAGES")
        for idx,(t,a,_) in enumerate(story):
            if st.button(f"Generate {i}-{idx}"):
                img_prompt = build_image_prompt(a)
                img = generate_image(img_prompt)
                if img:
                    st.image(img)

        # TIKTOK
        st.markdown("### 💰 CONTENT")
        st.code(f"""
Caption:
{caption()}

Hashtag:
{hashtag()}

Best time:
{post_time()}
""")

# ================= TRACK =================
st.markdown("---")
st.markdown("## 📊 TRACK VIDEO")

vid = st.text_input("Video ID")
hook_used = st.text_input("Hook used")
views = st.number_input("Views",0)

if st.button("SAVE RESULT"):
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
st.markdown("## 🔥 UPDATE TREND")

new_hook = st.text_input("New hook")

if st.button("ADD HOOK"):
    data = load_json(TREND_FILE, [])
    data.append(new_hook)
    save_json(TREND_FILE,data)
    st.success("Added!")
