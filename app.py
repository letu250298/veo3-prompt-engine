import streamlit as st
import requests
import base64
import os
import time

# =========================
# CONFIG
# =========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ Missing OPENAI_API_KEY (set trong Secrets)")
    st.stop()

API_URL = "https://api.openai.com/v1/responses"

# =========================
# UI
# =========================
st.set_page_config(page_title="Affiliate AI Generator", layout="wide")

st.title("🚀 Affiliate AI Generator (Stable Version)")

col1, col2 = st.columns(2)

with col1:
    character_img = st.file_uploader("📸 Ảnh nhân vật", type=["png", "jpg", "jpeg"])

with col2:
    product_img = st.file_uploader("📦 Ảnh sản phẩm", type=["png", "jpg", "jpeg"])

num_scripts = st.slider("🎬 Số kịch bản", 1, 10, 3)
duration = st.selectbox("⏱ Độ dài", ["8s", "16s", "24s", "32s"])

generate = st.button("🔥 Generate")

# =========================
# UTIL
# =========================
def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")

def call_api(input_data):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(
            API_URL,
            headers=headers,
            json={
                "model": "gpt-4o-mini",
                "input": input_data
            },
            timeout=30
        )

        # Debug status
        if res.status_code != 200:
            return f"❌ API Error {res.status_code}: {res.text}"

        data = res.json()

        if "error" in data:
            return f"❌ {data['error']['message']}"

        # Lấy text an toàn
        try:
            return data["output"][0]["content"][0]["text"]
        except:
            return f"❌ Unexpected response: {data}"

    except Exception as e:
        return f"❌ Exception: {str(e)}"

# =========================
# AI FUNCTIONS
# =========================
def analyze_product(image_base64):

    prompt = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Phân tích sản phẩm từ ảnh: tên, công dụng, USP, khách hàng, pain point, 5 angle TikTok"
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                }
            ]
        }
    ]

    result = call_api(prompt)

    return result if result else "❌ Không phân tích được"

def generate_script(analysis, duration, history):

    prompt = f"""
Bạn là TikTok creator 2026.

Thông tin sản phẩm:
{analysis}

Viết kịch bản {duration}:
- Hook mạnh
- Giọng nữ miền Nam
- Tự nhiên
- Không trùng: {history}

Có CTA

MASTER LOCK:
- Giữ nguyên nhân vật
- Giữ nguyên sản phẩm

Không text overlay
"""

    return call_api(prompt)

# =========================
# MAIN
# =========================
if generate:

    if not product_img or not character_img:
        st.warning("❗ Upload đủ ảnh")
        st.stop()

    product_base64 = encode_image(product_img)

    # ===== STEP 1 =====
    with st.spinner("🧠 Đang phân tích sản phẩm..."):
        analysis = analyze_product(product_base64)

    if not analysis or "❌" in str(analysis):
        st.error(analysis)
        st.stop()

    st.subheader("📊 Product Insight")
    st.write(analysis)

    # ===== STEP 2 =====
    st.subheader("🎬 Scripts")

    history = []

    for i in range(num_scripts):

        with st.spinner(f"Script {i+1}..."):
            script = generate_script(analysis, duration, history)

        if not script or "❌" in str(script):
            st.error(script)
            continue

        history.append(script[:200])

        st.markdown("---")
        st.subheader(f"🎬 Script {i+1}")
        st.code(script)
