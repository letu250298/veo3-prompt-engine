import streamlit as st
import random, json, os, base64
from datetime import datetime
import pandas as pd
import openai

openai.api_key = st.secrets.get("OPENAI_API_KEY","")

DATA_FILE = "data.json"

st.set_page_config(layout="wide")
st.title("💰 FINAL BOSS SELLING SYSTEM")

# ================= LOAD =================
def load_json(path, default):
    if os.path.exists(path):
        with open(path,"r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path,"w") as f:
        json.dump(data,f)

# ================= INPUT =================
st.sidebar.title("INPUT")

product = st.sidebar.file_uploader("Product", type=["png","jpg"])
customer = st.sidebar.selectbox("Customer",[
    "Sinh viên",
    "Dân văn phòng",
    "Người hay đi du lịch",
    "Người lười"
])

variants = st.sidebar.slider("Videos",1,5,3)
scale = st.sidebar.checkbox("AUTO SCALE")

# ================= PRODUCT AI =================
def analyze_product(img):
    if not img or not openai.api_key:
        return {
            "feature":"đa năng",
            "benefit":"tiện lợi",
            "pain":"hay quên đồ"
        }

    base64_img = base64.b64encode(img.read()).decode()

    res = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"user",
                "content":[
                    {"type":"text","text":"Phân tích sản phẩm: feature, benefit, pain point (JSON)"},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_img}"}}
                ]
            }
        ]
    )

    try:
        return json.loads(res.choices[0].message.content)
    except:
        return {"feature":"đa năng","benefit":"tiện","pain":"quên đồ"}

# ================= HOOK =================
def hook(insight, customer):
    pain = insight["pain"]
    return random.choice([
        f"{customer} mà hay bị {pain} thì coi cái này",
        f"Mình từng bị {pain} cho tới khi dùng cái này",
        f"Ai bị {pain} chắc hiểu cảm giác này"
    ])

# ================= STORY =================
def story(h,insight):
    return [
        ("0-3s","Hook",h),
        ("3-6s","Pain",f"Trước giờ mình bị {insight['pain']}"),
        ("6-10s","Feature",f"Cái này có {insight['feature']}"),
        ("10-15s","Benefit",f"{insight['benefit']} cực kỳ"),
        ("15-20s","CTA","Mua liền luôn")
    ]

# ================= GENERATE =================
if st.button("🚀 GENERATE MONEY CONTENT"):

    insight = analyze_product(product)

    st.success(f"🧠 Insight: {insight}")

    for i in range(variants):

        st.markdown(f"## 🎬 VIDEO {i+1}")

        h = hook(insight, customer)
        s = story(h, insight)

        for t,a,d in s:
            st.write(f"{t} | {d}")

        st.code(f"""
MASTER LOCK
IDENTITY LOCK
PRODUCT LOCK

SCENES:
{s}

NEGATIVE:
no text
""")

# ================= TRACK =================
st.markdown("---")
st.markdown("## 📊 TRACK")

vid = st.text_input("Video ID")
hook_used = st.text_input("Hook")
views = st.number_input("Views",0)

if st.button("SAVE"):
    data = load_json(DATA_FILE, [])
    data.append({"hook":hook_used,"views":views})
    save_json(DATA_FILE,data)
    st.success("Saved")

# ================= DASHBOARD =================
data = load_json(DATA_FILE, [])

if data:
    df = pd.DataFrame(data)
    st.bar_chart(df.groupby("hook")["views"].mean())
