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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ Missing OPENAI_API_KEY")
    st.stop()

API_URL = "https://api.openai.com/v1/responses"

# =========================
# UI
# =========================
st.set_page_config(page_title="Affiliate AI Generator PRO", layout="wide")

st.title("🚀 Affiliate AI Generator (Production Ready)")

col1, col2 = st.columns(2)

with col1:
    character_img = st.file_uploader("📸 Ảnh nhân vật", type=["png", "jpg", "jpeg"])

with col2:
    product_img = st.file_uploader("📦 Ảnh sản phẩm", type=["png", "jpg", "jpeg"])

num_scripts = st.slider("🎬 Số lượng kịch bản", 1, 10, 3)
duration = st.selectbox("⏱ Độ dài", ["8s", "16s", "24s", "32s"])

generate = st.button("🔥 Generate")

# =========================
# UTIL
# =========================
def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")

def call_api(input_data, retries=3):

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    for attempt in range(retries):
        try:
            res = requests.post(
                "https://api.openai.com/v1/responses",
                headers=headers,
                json={
                    "model": "gpt-4.1-mini",
                    "input": input_data
                }
            )

            # Nếu request fail
            if res.status_code != 200:
                if res.status_code == 429:
                    time.sleep(2)
                    continue
                return f"❌ API Error {res.status_code}: {res.text}"

            data = res.json()

            if "error" in data:
                return f"❌ {data['error']['message']}"

            try:
                return data["output"][0]["content"][0]["text"]
            except:
                return f"❌ Unexpected response: {data}"

        except Exception as e:
            if attempt == retries - 1:
                return f"❌ Exception: {str(e)}"
            time.sleep(1)

    return "❌ Failed after retries"

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
                    "text": "Phân tích sản phẩm từ ảnh: tên, công dụng, USP, khách hàng, pain point, 5 angle viral TikTok"
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                }
            ]
        }
    ]

    return call_api(prompt)

def generate_script(analysis, duration, history):

    prompt_text = f"""
Bạn là top TikTok creator 2026.

Thông tin sản phẩm:
{analysis}

Yêu cầu:
- Viết kịch bản video {duration}
- Hook cực mạnh 3s đầu
- Giọng nữ miền Nam, tự nhiên
- Đúng pain point
- Không chung chung
- KHÔNG trùng các kịch bản trước: {history}

Format:
- Scene rõ ràng
- Có CTA

MASTER LOCK:
- Nhân vật giữ nguyên 100%
- Sản phẩm giữ nguyên 100%
- Không thay đổi hình dạng, màu sắc

NO:
- text overlay
- subtitles
- UI
"""

    return call_api(prompt_text)

# =========================
# MAIN
# =========================
if generate:

    if not product_img or not character_img:
        st.warning("❗ Vui lòng upload đủ ảnh")
        st.stop()

    product_base64 = encode_image(product_img)

    # STEP 1: ANALYSIS
    with st.spinner("🧠 AI đang phân tích sản phẩm..."):
        analysis = analyze_product(product_base64)

    if "❌" in analysis:
        st.error(analysis)
        st.stop()

    st.subheader("📊 Phân tích sản phẩm")
    st.write(analysis)

    # STEP 2: GENERATE SCRIPTS
    st.subheader("🎬 Kịch bản")

    history = []

    for i in range(num_scripts):

        with st.spinner(f"Đang tạo kịch bản {i+1}..."):
            script = generate_script(
                analysis,
                duration,
                history
            )

        if "❌" in script:
            st.error(script)
            continue

        history.append(script[:200])

        st.markdown("---")
        st.subheader(f"🎬 Script {i+1}")
        st.code(script)
