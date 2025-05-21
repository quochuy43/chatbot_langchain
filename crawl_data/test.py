import requests
import json

url = "https://tiki.vn/api/personalish/v1/blocks/listings"
params = {
    "limit": 1,          # Lấy 1 sản phẩm thôi để dễ quan sát
    "category": 1789,    # Ví dụ: Điện thoại - Máy tính bảng
    "page": 1
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    first_item = data['data'][0]
    print(json.dumps(first_item, indent=2, ensure_ascii=False))
else:
    print("Không lấy được dữ liệu từ Tiki.")
