import streamlit as st
import base64
import requests
import random

# =========================
# CONFIG
# =========================
OPENAI_API_KEY = "YOUR_API_KEY"
API_URL = "https://api.openai.com/v1/chat/completions"

st.set_page_config(page_title="Affiliate AI Generator PRO", layout="wide")

st.title("🚀 Affiliate AI Generator PRO (FINAL BOSS)")
st.write("Upload ảnh → AI tự hiểu sản phẩm → tạo kịch bản viral TikTok")

# =========================
# INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    character_img = st.file_uploader("📸 Ảnh nhân vật", type=["png","jpg","jpeg"])

with col2:
    product_img = st.file_uploader("📦 Ảnh sản phẩm", type=["png","jpg","jpeg"])

num_scripts = st.slider("🎬 Số lượng kịch bản", 1, 20, 5)

duration = st.selectbox("⏱ Độ dài video", [
    "8s","16s","24s","32s","40s","48s","56s"
])

style = st.selectbox("🎯 Phong cách", [
    "Auto (AI chọn)",
    "Bán hàng mạnh",
    "Review chân thật",
    "Hài hước",
    "Cinematic ads"
])

generate = st.button("🔥 Generate")

# =========================
# UTIL
# =========================
def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")

def call_api(messages, max_tokens=1000):

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1",
        "messages": messages,
        "max_tokens": max_tokens
    }

    try:
        res = requests.post(API_URL, headers=headers, json=data)

        # Debug raw response
        if res.status_code != 200:
            return f"❌ API Error {res.status_code}: {res.text}"

        json_res = res.json()

        # Nếu API trả về lỗi
        if "error" in json_res:
            return f"❌ API Error: {json_res['error']['message']}"

        # Nếu thiếu choices
        if "choices" not in json_res:
            return f"❌ Unexpected response: {json_res}"

        return json_res["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Exception: {str(e)}"
# =========================
# STEP 1: ANALYZE PRODUCT
# =========================
def analyze_product(image_base64):

    prompt = """
Bạn là chuyên gia TikTok Affiliate 2026.

Phân tích sản phẩm từ ảnh:

Trả về:
- Tên sản phẩm
- Loại sản phẩm
- Công dụng
- 5 USP bán hàng
- Khách hàng mục tiêu
- Pain point
- Tình huống sử dụng
- 5 góc nội dung viral TikTok
- 3 format phù hợp nhất

Viết NGẮN – CHÍNH XÁC – BÁN ĐƯỢC HÀNG.
"""

    return call_api([{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]
    }], 800)

# =========================
# STEP 2: GENERATE SCRIPT
# =========================
def generate_script(analysis, duration, style, history):

    prompt = f"""
Bạn là top TikTok creator affiliate.

Thông tin sản phẩm:
{analysis}

Yêu cầu:
- Viết kịch bản {duration}
- Hook cực mạnh 3s đầu
- Giọng tự nhiên (nữ, miền Nam)
- Đúng pain point
- Không chung chung
- Không giống các kịch bản trước: {history}

Style: {style}

Format:
- Scene rõ ràng
- Có CTA

THÊM MASTER LOCK:

Character MUST giữ nguyên như ảnh
Product MUST giữ nguyên như ảnh

NO:
- text overlay
- subtitles
- UI
"""

    return call_api([{"role": "user", "content": prompt}], 1200)

# =========================
# MAIN
# =========================
if generate:

    if not product_img or not character_img:
        st.warning("❗ Vui lòng upload đủ ảnh")
    else:

        # Encode image
        product_base64 = encode_image(product_img)

        # STEP 1: ANALYSIS
        with st.spinner("🧠 AI đang phân tích sản phẩm..."):
            analysis = analyze_product(product_base64)

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
                    style,
                    history
                )

                history.append(script[:200])

                st.markdown(f"---")
                st.subheader(f"🎬 Script {i+1}")
                st.code(script)
