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


## Tổng hợp các nội dung phân tích

| STT | Nội dung | Thành viên |
|---:|---|---|
| 4.1 | Phân tích số lượng trò chơi theo thời gian | 25410185 |
| 4.2 | Phân tích doanh số toàn cầu theo thời gian | 25410185 |
| 4.3 | Phân tích doanh số theo thể loại | 25410210 |
| 4.4 | Doanh số trung bình theo thể loại | 25410210 |
| 4.5 | Phân tích theo nền tảng (tổng doanh số và phân phối) | 25410210 |
| 4.6 | Phân tích theo nhà phát hành | 25410185 |
| 4.7 | Phân tích sự khác biệt giữa các khu vực (tổng, heatmap, phân phối) | 25410186 |
| 4.8 | Doanh số khu vực theo thời gian | 25410186 |
| 4.9 | Phân tích các trò chơi có doanh số cao nhất | 25410186 |
| 4.10 | Phân phối doanh số của các trò chơi | 25410186 |

## Chi tiết công việc

### 25410185 – Dữ liệu, thời gian và nhà phát hành

Phụ trách xử lý dữ liệu ban đầu, phân tích theo thời gian và nhà phát hành.

- Xử lý dữ liệu trong:
  - `analysis/data_loader.py`
  - `analysis/preprocessing.py`
- Xây dựng các hàm trong `analysis.py`:
  - `analyze_games_per_year`
  - `analyze_global_sales_per_year`
  - `analyze_top_publishers`
- Phụ trách các route:
  - `/overview`
  - `/time-analysis`
  - `/publisher-analysis`
- Phụ trách các template:
  - `overview.html`
  - `time_analysis.html`
  - `publisher_analysis.html`
- Phụ trách biểu đồ:
  - Số lượng trò chơi theo thời gian.
  - Doanh số toàn cầu theo thời gian.
  - Top 10 nhà phát hành.


### 25410210 – Thể loại, nền tảng và phương pháp

Phụ trách các phân tích theo thể loại và nền tảng, cùng phần phương pháp trong báo cáo.

- Xây dựng các hàm trong `analysis.py`:
  - `analyze_genre_summary` (bảng tổng hợp thể loại)
  - `analyze_genre_sales`
  - `analyze_genre_average_sales`
  - `analyze_platform_sales`
  - `analyze_platform_distribution`
- Phụ trách các route:
  - `/genre-analysis`
  - `/platform-analysis`
- Phụ trách các template:
  - `genre_analysis.html`
  - `platform_analysis.html`
- Phụ trách biểu đồ:
  - Doanh số theo thể loại.
  - Doanh số trung bình theo thể loại.
  - Doanh số theo nền tảng.
  - Boxplot `Global_Sales` theo nền tảng.

### 25410186 – Khu vực, Top games, phân phối doanh số và tích hợp

Phụ trách các phân tích theo khu vực, các trò chơi có doanh số cao, phân phối doanh số và phần tích hợp ứng dụng.

- Xây dựng các hàm trong `analysis.py`:
  - `analyze_region_totals`
  - `analyze_genre_region_heatmap`
  - `analyze_region_distribution`
  - `analyze_region_sales_over_time`
  - `analyze_top_games`
  - `analyze_sales_distribution`
  - `run_all_analysis`
- Phụ trách:
  - `/` (trang Index)
  - `/region-analysis`
  - `/distribution-analysis`
  - `app.py`
- Phụ trách các template:
  - `base.html`
  - `index.html`
  - `region_analysis.html`
  - `distribution_analysis.html`
- Phụ trách các thành phần:
  - `style.css`
  - `dashboard.js`
  - `requirements.txt`
  - `README.md`
- Phụ trách biểu đồ:
  - Heatmap thể loại và khu vực.
  - Violinplot doanh số theo khu vực.
  - Doanh số khu vực theo thời gian.
  - Top các trò chơi có doanh số cao nhất.
  - Histogram `Global_Sales`.
  - Boxplot `Global_Sales` theo thể loại.

## Lưu ý khi làm việc chung

- `analysis/analysis.py`, `routes/analysis.py` và `routes/dashboard.py` là file dùng chung: mỗi người chỉ sửa hàm/route của mình.



