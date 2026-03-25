import streamlit as st
import base64
import requests
import os
import time
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================
load_dotenv()
OPENAI_API_KEY =  os.getenv("OPENAI_API_KEY")
st.write("KEY:", OPENAI_API_KEY)
if not OPENAI_API_KEY:
    st.error("❌ Missing OPENAI_API_KEY")
    st.stop()

API_URL = "https://api.openai.com/v1/chat/completions"

st.set_page_config(page_title="Affiliate AI Generator PRO", layout="wide")

st.title("🚀 Affiliate AI Generator (Production Ready)")

# =========================
# INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    character_img = st.file_uploader("Ảnh nhân vật", type=["png","jpg","jpeg"])

with col2:
    product_img = st.file_uploader("Ảnh sản phẩm", type=["png","jpg","jpeg"])

num_scripts = st.slider("Số kịch bản", 1, 10, 3)
duration = st.selectbox("Độ dài", ["8s","16s","24s","32s"])

generate = st.button("🔥 Generate")

# =========================
# UTIL
# =========================
def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")

def call_api(messages):

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    res = requests.post(
        "https://api.openai.com/v1/responses",
        headers=headers,
        json={
            "model": "gpt-4.1-mini",
            "input": messages
        }
    )

    data = res.json()

    if "error" in data:
        return f"❌ {data['error']['message']}"

    return data["output"][0]["content"][0]["text"]

# =========================
# AI FUNCTIONS
# =========================
def analyze_product(image_base64):

    prompt = "Phân tích sản phẩm từ ảnh, đưa ra USP, khách hàng, pain point"

    return call_api([
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                }
            ]
        }
    ])
def generate_script(analysis, duration, history):
    prompt = f"""
Dựa vào:
{analysis}

Viết kịch bản TikTok {duration}

Hook mạnh
Không trùng: {history}

Thêm MASTER LOCK giữ sản phẩm + nhân vật
"""

    return call_api([{"role": "user", "content": prompt}])

# =========================
# MAIN
# =========================
if generate:

    if not product_img or not character_img:
        st.warning("Upload đủ ảnh")
        st.stop()

    product_base64 = encode_image(product_img)

    with st.spinner("Đang phân tích sản phẩm..."):
        analysis = analyze_product(product_base64)

    if "❌" in analysis:
        st.error(analysis)
        st.stop()

    st.subheader("📊 Product Insight")
    st.write(analysis)

    history = []

    st.subheader("🎬 Scripts")

    for i in range(num_scripts):

        with st.spinner(f"Script {i+1}..."):
            script = generate_script(analysis, duration, history)

        if "❌" in script:
            st.error(script)
            continue

        history.append(script[:150])

        st.markdown("---")
        st.code(script)
