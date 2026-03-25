import base64
import requests

OPENAI_API_KEY = "YOUR_API_KEY"

# =========================
# IMAGE → BASE64
# =========================
def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")

# =========================
# STEP 1: ANALYZE PRODUCT
# =========================
def analyze_product(image_base64):

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = """
Bạn là chuyên gia TikTok Affiliate 10 năm kinh nghiệm.

Phân tích sản phẩm từ ảnh và trả về:

1. Tên sản phẩm
2. Loại sản phẩm
3. Công dụng chính
4. 5 điểm bán hàng (USP)
5. Khách hàng mục tiêu
6. Pain point khách hàng
7. Tình huống sử dụng
8. Format TikTok phù hợp nhất (3 format)

Viết ngắn gọn, đúng insight, bán được hàng.
"""

    data = {
        "model": "gpt-4.1",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 800
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]

# =========================
# STEP 2: GENERATE SCRIPT
# =========================
def generate_script_with_ai(product_analysis, duration):

    prompt = f"""
Bạn là top TikTok creator 2026.

Dựa vào thông tin sản phẩm sau:

{product_analysis}

Hãy tạo 1 kịch bản video {duration}:
- Hook cực mạnh 3s đầu
- Nội dung tự nhiên, giống người thật
- Không generic
- Đúng pain point
- Có CTA nhẹ

Đảm bảo KHÔNG trùng format với các kịch bản khác.

Thêm MASTER LOCK để:
- giữ nhân vật không đổi
- giữ sản phẩm không biến dạng
"""

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]
