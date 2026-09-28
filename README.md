# IE313_25410185-25410186-25410210
Đồ án Phân tích dữ liệu trực quan

## Đề tài: *"Phân tích thăm dò dữ liệu trò chơi điện tử bằng thư viện Seaborn"*

## Nguồn dữ liệu

Tệp `vgsales.csv` — Video Game Sales dataset.
https://www.kaggle.com/datasets/gregorut/videogamesales?select=vgsales.csv


## Phân công:
25410186 - Nguyễn Tấn Đạt - Viết báo cáo

25410185 - Nguyễn Phong Đạt - Quay video demo

25410210 - Lương Bá Minh Hiếu - Làm slide


## Tổng hợp 8 nội dung phân tích

| STT | Nội dung | Thành viên |
|---:|---|---|
| 4.1 | Phân tích số lượng trò chơi theo thời gian | 25410185 |
| 4.2 | Phân tích doanh số toàn cầu theo thời gian | 25410185 |
| 4.3 | Phân tích doanh số theo thể loại | 25410210 |
| 4.4 | Doanh số trung bình theo thể loại | 25410210 |
| 4.5 | Phân tích theo nền tảng | 25410210 |
| 4.6 | Phân tích sự khác biệt giữa các khu vực | 25410186 |
| 4.7 | Doanh số khu vực theo thời gian | 25410186 |
| 4.8 | Phân tích các trò chơi có doanh số cao nhất | 25410186 |

## Chi tiết công việc

### 25410185 – Dữ liệu và thời gian

Phụ trách phần xử lý dữ liệu ban đầu và các phân tích liên quan đến thời gian.

- Xử lý dữ liệu trong:
  - `analysis/data_loader.py`
  - `analysis/preprocessing.py`
- Xây dựng các hàm:
  - `analyze_games_per_year`
  - `analyze_global_sales_per_year`
- Phụ trách các route:
  - `/overview`
  - `/time-analysis`
- Phụ trách các template:
  - `overview.html`
  - `time_analysis.html`
- Phụ trách biểu đồ:
  - `fig1`: Số lượng trò chơi theo thời gian.
  - `fig2`: Doanh số toàn cầu theo thời gian.

### 25410210 – Thể loại và nền tảng

Phụ trách các phân tích liên quan đến thể loại trò chơi và nền tảng.

- Xây dựng các hàm trong `analysis.py`:
  - `analyze_genre_sales`
  - `analyze_genre_average_sales`
  - `analyze_platform_sales`
- Phụ trách các route:
  - `/genre-analysis`
  - `/platform-analysis`
- Phụ trách các template:
  - `genre_analysis.html`
  - `platform_analysis.html`
- Phụ trách biểu đồ:
  - `fig3`: Doanh số theo thể loại.
  - `fig4`: Doanh số trung bình theo thể loại.
  - `fig5`: Doanh số theo nền tảng.

### 25410186 – Khu vực và tích hợp

Phụ trách các phân tích liên quan đến khu vực, các trò chơi có doanh số cao và phần tích hợp ứng dụng.

- Xây dựng các hàm trong `analysis.py`:
  - `analyze_genre_region_heatmap`
  - `analyze_region_sales_over_time`
  - `analyze_top_games`
  - `run_all_analysis`
- Phụ trách:
  - `/` (trang Index)
  - `/region-analysis`
  - `app.py`
- Phụ trách các template:
  - `base.html`
  - `index.html`
  - `region_analysis.html`
- Phụ trách các thành phần:
  - `style.css`
  - `dashboard.js`
  - `requirements.txt`
  - `README.md`
- Phụ trách biểu đồ:
  - `fig6`: Heatmap thể loại và khu vực.
  - `fig7`: Doanh số khu vực theo thời gian.
  - `fig8`: Top các trò chơi có doanh số cao nhất.


## Cấu trúc phối hợp

```text
                    vgsales.csv
                         │
              ┌──────────┴──────────┐
              │                     │
         25410185               25410210
  Dữ liệu + Thời gian      Thể loại + Nền tảng
              │                     │
              └──────────┬──────────┘
                         │
                    analysis.py
                         │
                         ▼
                     25410186
             Khu vực + Tích hợp Flask
                         │
                         ▼
                  Web Dashboard
```

