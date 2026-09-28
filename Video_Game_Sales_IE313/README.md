# Video Game Sales IE313 — Flask EDA Dashboard

Đồ án **IE313 — Phân tích dữ liệu**

Đề tài *"Phân tích thăm dò dữ liệu trò chơi điện tử bằng thư viện Seaborn"*. 

Xây dựng Dashboard trình bày các kết quả phân tích thăm dò dữ liệu (EDA)

## Nguồn dữ liệu

Tệp `vgsales.csv` — Video Game Sales dataset.
https://www.kaggle.com/datasets/gregorut/videogamesales?select=vgsales.csv

4.1. Phân tích số lượng trò chơi theo thời gian

4.2. Phân tích doanh số toàn cầu theo thời gian

4.3. Phân tích doanh số theo thể loại

4.4. Doanh số trung bình theo thể loại

4.5. Phân tích theo nền tảng

4.6. Phân tích sự khác biệt giữa các khu vực

4.7. Doanh số khu vực theo thời gian

4.8. Phân tích các trò chơi có doanh số cao nhất

## Kiến trúc dự án

```
Video_Game_Sales_IE313/
├── app.py                     # Điểm khởi chạy Flask app
├── requirements.txt
├── README.md
├── data/
│   └── vgsales.csv            # Dữ liệu nguồn
├── analysis/
│   ├── __init__.py
│   ├── data_loader.py         # Đọc & cache dữ liệu CSV
│   ├── preprocessing.py       # Chuẩn hoá kiểu dữ liệu, thống kê missing values
│   └── analysis.py            # 8 hàm EDA + vẽ biểu đồ Seaborn/Matplotlib
├── routes/
│   ├── __init__.py
│   ├── dashboard.py           # Route: / (index), /overview
│   └── analysis.py            # Route: /time-analysis, /genre-analysis,
│                               #        /platform-analysis, /region-analysis
├── templates/
│   ├── base.html               # Layout chung (sidebar + topbar)
│   ├── index.html              # Trang chủ
│   ├── overview.html           # Mô tả bộ dữ liệu
│   ├── time_analysis.html      # 4.1, 4.2
│   ├── platform_analysis.html  # 4.5
│   ├── genre_analysis.html     # 4.3, 4.4
│   └── region_analysis.html    # 4.6, 4.7, 4.8
└── static/
    ├── css/style.css
    ├── js/dashboard.js
    └── images/                 # fig1..fig8 .png được tạo tự động khi chạy app
```

## Cài đặt & chạy ứng dụng

```bash
cd Video_Game_Sales_IE313
python -m venv venv
source venv/bin/activate      
# Windows: venv\Scripts\activate hoặc terminal pycharm .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Sau khi chạy, mở trình duyệt tại: **http://127.0.0.1:5000**

## Các trang trong Dashboard

| Route                | Nội dung                                                              | Mục báo cáo |
|-----------------------|------------------------------------------------------------------------|-------------|
| `/`                  | Trang chủ, giới thiệu đề tài và điều hướng                              | 1           |
| `/overview`          | Mô tả bộ dữ liệu, kiểu dữ liệu, số lượng giá trị thiếu                   | 2           |
| `/time-analysis`     | Số lượng trò chơi theo năm; Tổng doanh số toàn cầu theo năm              | 4.1, 4.2    |
| `/genre-analysis`    | Tổng doanh số theo thể loại; Doanh số trung bình theo thể loại           | 4.3, 4.4    |
| `/platform-analysis` | Top 10 nền tảng theo tổng doanh số toàn cầu                              | 4.5         |
| `/region-analysis`   | Heatmap thể loại-khu vực; Doanh số khu vực theo thời gian; Top 10 game   | 4.6, 4.7, 4.8 |

## Xử lý dữ liệu

- Cột `Year` và các cột doanh số (`NA_Sales`, `EU_Sales`, `JP_Sales`,
  `Other_Sales`, `Global_Sales`) được chuyển về kiểu số.
- Giá trị thiếu ở `Year` (271 bản ghi, ~1,63%) và `Publisher` (58 bản ghi,
  ~0,35%) **không bị điền giá trị thay thế**.
- Với các phân tích theo thời gian (4.1, 4.2, 4.7), các bản ghi thiếu `Year`
  chỉ bị loại trừ cục bộ khỏi phép tổng hợp theo năm; dữ liệu tổng thể vẫn
  được giữ nguyên cho các phân tích khác (Genre, Platform, Top Games).
- Dữ liệu được đọc và tiền xử lý một lần duy nhất và cache lại (`lru_cache`)
  để tránh đọc lại CSV mỗi khi chuyển trang.

## Công nghệ sử dụng

- **Flask** — tổ chức route và render template (kiến trúc Blueprint).
- **Pandas** — đọc, tiền xử lý và tổng hợp dữ liệu.
- **Seaborn / Matplotlib** — trực quan hóa (bar chart, line chart, heatmap).
- **Jinja2 + CSS thuần** — giao diện Dashboard, không phụ thuộc framework
  frontend ngoài.


