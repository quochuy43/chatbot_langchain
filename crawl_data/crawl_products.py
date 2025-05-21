import requests

url = "https://tiki.vn/api/personalish/v1/blocks/listings"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}

categories = {
    "Nhà sách": 8322,
    "Hàng hóa gia đình": 1883,
    "Điện thoại và Laptop": 1789,
    "Ô tô - Xe máy - Xe đạp": 8594,
    "Thời trang": 27498
}

all_products_by_category = {}

for category_name, category_id in categories.items():
    for page in range(1, 3):
        params = {
            "limit": 20,
            "category": category_id,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            products = []
            for item in data.get('data', []):
                products.append({
                    "name": item.get("name"),
                    "price": item.get("price"),
                    "link": f"https://tiki.vn/{item.get('url_path')}",
                    "rating": item.get("rating_average"),
                    "review_count": item.get("review_count"),
                    "brand": item.get("brand", {}).get("name"),
                })
            all_products_by_category[category_name] = products
        else:
            print("Failed to crawl data")

# for idx, product in enumerate(all_products, start=1):
#     print(f"{idx}. {product['name']}")
#     print(f"   Giá: {product['gia']}")
#     print(f"   Link: {product['link']}")
#     print(f"   Danh mục: {product['category']}")
#     print(f"   Thương hiệu: {product['thuong_hieu']}")
#     print(f"   Đánh giá: {product['danh_gia']} ({product['so_luot_danh_gia']} lượt)\n")

# Create Markdown content
output_lines = ["# Thông tin sản phẩm\n"]

for category_name, products in all_products_by_category.items():
    output_lines.append(f"## {category_name}\n")
    for product in products:
        output_lines.append(f"### {product['name']}\n")
        output_lines.append(f"**Tên sản phẩm:** {product['name']}\n")
        output_lines.append(f"**Giá:** {product['price']:,} VNĐ" if product['price'] else "**Giá:** Đang cập nhật\n")
        output_lines.append(f"**Đường dẫn đến sản phẩm chi tiết:** {product['link']}\n")
        output_lines.append(f"**Đánh giá của khách hàng:** {product['rating']}\n")
        output_lines.append(f"**Số lượt đánh giá của khách hàng:** {product['review_count']}\n")
        output_lines.append(f"**Thương hiệu:** {product['brand']}\n")

with open("products.md", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

    