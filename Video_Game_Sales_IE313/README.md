# Video Game Sales IE313 — Flask EDA Dashboard

Đồ án **IE313 — Phân tích dữ liệu**

Đề tài *"Phân tích thăm dò dữ liệu trò chơi điện tử bằng thư viện Seaborn"*. 

Xây dựng Dashboard trình bày các kết quả phân tích thăm dò dữ liệu (EDA)

## Nguồn dữ liệu

Tệp `vgsales.csv` — Video Game Sales dataset.
https://www.kaggle.com/datasets/gregorut/videogamesales?select=vgsales.csv

## Tổng hợp các nội dung phân tích

| STT  | Nội dung                                                    |
|-----:|--------------------------------------------------------------|
| 4.1  | Phân tích số lượng trò chơi theo thời gian                    |
| 4.2  | Phân tích doanh số toàn cầu theo thời gian                    |
| 4.3  | Phân tích doanh số theo thể loại                              |
| 4.4  | Doanh số trung bình theo thể loại                             |
| 4.5  | Phân tích theo nền tảng (tổng doanh số và phân phối)          |
| 4.6  | Phân tích theo nhà phát hành                                  |
| 4.7  | Phân tích sự khác biệt giữa các khu vực (tổng, heatmap, phân phối) |
| 4.8  | Doanh số khu vực theo thời gian                               |
| 4.9  | Phân tích các trò chơi có doanh số cao nhất                   |
| 4.10 | Phân phối doanh số của các trò chơi                           |

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
│   └── analysis.py            # 13 biểu đồ EDA Seaborn/Matplotlib + bảng số liệu
├── routes/
│   ├── __init__.py
│   ├── dashboard.py           # Route: / (index), /overview
│   └── analysis.py            # Route: /time-analysis, /genre-analysis,
│                               #        /platform-analysis, /publisher-analysis,
│                               #        /region-analysis, /distribution-analysis
├── templates/
│   ├── base.html                    # Layout chung (sidebar + topbar)
│   ├── index.html                   # Trang chủ
│   ├── overview.html                # Mô tả bộ dữ liệu
│   ├── time_analysis.html           # 4.1, 4.2
│   ├── genre_analysis.html          # 4.3, 4.4
│   ├── platform_analysis.html       # 4.5
│   ├── publisher_analysis.html      # 4.6
│   ├── region_analysis.html         # 4.7, 4.8, 4.9
│   └── distribution_analysis.html   # 4.10
└── static/
    ├── css/style.css
    ├── js/dashboard.js
    └── images/                 # fig1..fig13 .png được tạo tự động khi chạy app
```

## Cài đặt & chạy ứng dụng

```bash
cd Video_Game_Sales_IE313
python -m venv venv
source venv/bin/activate
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Sau khi chạy, mở trình duyệt tại: **http://127.0.0.1:5000**

Các hình `fig1_...png` đến `fig13_...png` trong `static/images/` được Seaborn/
Matplotlib tạo tự động ngay trong lần đầu người dùng mở mỗi trang phân tích
(không cần chạy script riêng trước).

## Các trang trong Dashboard

| Route                    | Nội dung                                                                    | Mục báo cáo |
|--------------------------|------------------------------------------------------------------------------|-------------|
| `/`                      | Trang chủ, giới thiệu đề tài và điều hướng                                    | 1           |
| `/overview`              | Mô tả bộ dữ liệu, thống kê mô tả, số lượng giá trị thiếu                      | 2           |
| `/time-analysis`         | Số lượng trò chơi theo năm; Tổng doanh số toàn cầu theo năm                   | 4.1, 4.2    |
| `/genre-analysis`        | Tổng doanh số và doanh số trung bình theo thể loại (kèm bảng số liệu)         | 4.3, 4.4    |
| `/platform-analysis`     | Top 10 nền tảng: tổng doanh số (barplot) và phân phối (boxplot)               | 4.5         |
| `/publisher-analysis`    | Top 10 nhà phát hành theo tổng doanh số toàn cầu                              | 4.6         |
| `/region-analysis`       | Tổng theo khu vực + heatmap; violinplot; khu vực theo thời gian; Top 10 game  | 4.7, 4.8, 4.9 |
| `/distribution-analysis` | Histogram Global_Sales, boxplot theo thể loại, thống kê mô tả                 | 4.10        |

## Đối chiếu file ảnh và hình trong báo cáo

| File ảnh                        | Hình trong báo cáo |
|----------------------------------|--------------------|
| `fig1_year_game_count.png`       | Hình 2             |
| `fig2_year_global_sales.png`     | Hình 3             |
| `fig3_genre_sales.png`           | Hình 4             |
| `fig4_genre_average_sales.png`   | Hình 5             |
| `fig5_platform_sales.png`        | Hình 6             |
| `fig12_platform_boxplot.png`     | Hình 7             |
| `fig11_top_publishers.png`       | Hình 8             |
| `fig6_genre_region_heatmap.png`  | Hình 9             |
| `fig13_region_violin.png`        | Hình 10            |
| `fig7_region_year.png`           | Hình 11            |
| `fig8_top_games.png`             | Hình 12            |
| `fig9_sales_distribution.png`    | Hình 13            |
| `fig10_genre_boxplot.png`        | Hình 14            |

(Hình 1 trong báo cáo là sơ đồ quy trình phân tích, không sinh từ code.)

## Xử lý dữ liệu

- Cột `Year` và các cột doanh số (`NA_Sales`, `EU_Sales`, `JP_Sales`,
  `Other_Sales`, `Global_Sales`) được chuyển về kiểu số.
- Giá trị thiếu ở `Year` (271 bản ghi, ~1,63%) và `Publisher` (58 bản ghi,
  ~0,35%) **không bị điền giá trị thay thế**.
- Với các phân tích theo thời gian (4.1, 4.2, 4.8), các bản ghi thiếu `Year`
  chỉ bị loại trừ cục bộ khỏi phép tổng hợp theo năm; dữ liệu tổng thể vẫn
  được giữ nguyên cho các phân tích khác (Genre, Platform, Publisher, Top
  Games). Tương tự, các bản ghi thiếu `Publisher` chỉ bị loại khỏi phân tích
  nhà phát hành (4.6).
- Dữ liệu được đọc và tiền xử lý một lần duy nhất và cache lại (`lru_cache`)
  để tránh đọc lại CSV mỗi khi chuyển trang.

## Công nghệ sử dụng

- **Flask** — tổ chức route và render template (kiến trúc Blueprint).
- **Pandas** — đọc, tiền xử lý và tổng hợp dữ liệu.
- **Seaborn / Matplotlib** — trực quan hóa (barplot, lineplot, heatmap,
  histplot, boxplot, violinplot).
- **Jinja2 + CSS thuần** — giao diện Dashboard, không phụ thuộc framework
  frontend ngoài.


