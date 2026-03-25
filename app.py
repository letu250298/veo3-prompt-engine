import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="TikTok Affiliate Script Generator PRO", layout="wide")

st.title("🚀 TikTok Affiliate Script Generator PRO (Veo 3 Ready)")
st.write("Tạo hàng loạt kịch bản affiliate chuẩn viral + khóa nhân vật & sản phẩm")

# =========================
# INPUT
# =========================

col1, col2 = st.columns(2)

with col1:
    character_img = st.file_uploader("Upload ảnh nhân vật", type=["png","jpg","jpeg"])
with col2:
    product_img = st.file_uploader("Upload ảnh sản phẩm", type=["png","jpg","jpeg"])

num_scripts = st.slider("Số lượng kịch bản", 1, 20, 5)

duration = st.selectbox("Độ dài video", [
    "8s","16s","24s","32s","40s","48s","56s"
])

format_option = st.selectbox("Chọn format", [
    "Auto (AI chọn)",
    "Review chân thật",
    "Unbox",
    "POV",
    "So sánh",
    "Story bán hàng",
    "Bắt trend TikTok",
    "Problem - Solution"
])

product_desc = st.text_area("Mô tả sản phẩm (key selling points)", "")

generate = st.button("🔥 Generate Scripts")

# =========================
# FORMAT LIBRARY (TREND 2026)
# =========================

formats = [
    "hook tò mò",
    "review thật",
    "mua vì tò mò",
    "ai cũng đang dùng",
    "so sánh trước sau",
    "pov tình huống",
    "bị hiểu lầm",
    "test thử",
    "reaction",
    "giải quyết vấn đề"
]

# =========================
# GENERATOR
# =========================

def generate_script(format_type, duration):
    
    hook_list = [
        "Ủa… sao ai cũng xài cái này vậy?",
        "Tui tưởng cái này vô dụng luôn á",
        "Mua vì tò mò… ai ngờ dính luôn",
        "Cái này mà không biết là phí luôn",
        "Ủa cái này là cái gì vậy trời?"
    ]
    
    hook = random.choice(hook_list)
    
    script = f"""
MASTER LOCK:
Mode: Image-to-Video using provided reference images only.
Character MUST remain identical to reference image.
Product MUST remain identical to reference product.
NO regeneration, NO redesign.

Audio:
Vietnamese female voice, natural, miền Nam, 25 tuổi.
Lip-sync accurate.

Format:
Vertical 9:16 TikTok

SCENE (0–{duration}):

HOOK:
"{hook}"

BODY:
Trải nghiệm sản phẩm theo format: {format_type}

CTA:
"Ai đang cần thì nên thử cái này."
"""
    
    return script

# =========================
# MAIN LOGIC
# =========================

if generate:

    if not product_desc:
        st.warning("Vui lòng nhập mô tả sản phẩm")
    else:
        st.success("Đang tạo kịch bản...")

        used_formats = []
        results = []

        for i in range(num_scripts):
            
            if format_option == "Auto (AI chọn)":
                available_formats = list(set(formats) - set(used_formats))
                if not available_formats:
                    available_formats = formats
                chosen_format = random.choice(available_formats)
                used_formats.append(chosen_format)
            else:
                chosen_format = format_option

            script = generate_script(chosen_format, duration)
            results.append((i+1, chosen_format, script))

        # =========================
        # OUTPUT
        # =========================

        for idx, fmt, sc in results:
            st.markdown(f"---")
            st.subheader(f"🎬 Script {idx} - Format: {fmt}")
            st.code(sc)
