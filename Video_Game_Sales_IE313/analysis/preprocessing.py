"""
preprocessing.py
-----------------
Tiền xử lý dữ liệu vgsales.csv theo đúng cách tiếp cận đã mô tả trong
báo cáo:
  - Chuyển các biến năm và doanh số về đúng kiểu dữ liệu số.
  - Thống kê giá trị thiếu trước khi phân tích (Year, Publisher).
  - KHÔNG tự ý điền giá trị thay thế cho Year bị thiếu.
  - Đối với các phân tích theo năm, loại bỏ các bản ghi thiếu Year
    khỏi phép tổng hợp (nhưng vẫn giữ nguyên trong dữ liệu tổng thể).
"""

import pandas as pd

NUMERIC_SALES_COLS = [
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales",
]

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hoá kiểu dữ liệu của DataFrame gốc.

    - Year: chuyển sang kiểu số (float), giữ NaN cho giá trị thiếu.
    - Các cột doanh số: đảm bảo kiểu float.
    - Loại bỏ các bản ghi trùng lặp hoàn toàn (nếu có).

    Dữ liệu KHÔNG bị loại bỏ dòng thiếu Year ở bước này; việc loại bỏ
    chỉ được thực hiện cục bộ trong các hàm phân tích theo thời gian,
    để không làm ảnh hưởng tới các phân tích không phụ thuộc Year
    (ví dụ phân tích theo Genre, Platform, Top Games).
    """
    data = df.copy()

    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    for col in NUMERIC_SALES_COLS:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.drop_duplicates()

    return data


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trả về bảng thống kê số lượng và tỷ lệ giá trị thiếu theo từng cột,
    dùng cho phần "Đặc điểm ban đầu của dữ liệu" trên Dashboard.
    """
    total = len(df)
    missing_count = df.isna().sum()
    missing_percent = (missing_count / total * 100).round(2)

    summary = pd.DataFrame(
        {
            "Cột": missing_count.index,
            "Số giá trị thiếu": missing_count.values,
            "Tỷ lệ (%)": missing_percent.values,
        }
    )
    summary = summary[summary["Số giá trị thiếu"] > 0].reset_index(drop=True)
    return summary


def get_dataset_overview(df: pd.DataFrame) -> dict:
    """
    Trả về các chỉ số tổng quan về bộ dữ liệu để hiển thị ở trang Overview:
    số bản ghi, số thuộc tính, số nền tảng, số thể loại, số nhà phát hành,
    khoảng năm, và bảng giá trị thiếu.
    """
    n_records, n_cols = df.shape
    n_platforms = df["Platform"].nunique()
    n_genres = df["Genre"].nunique()
    n_publishers = df["Publisher"].nunique(dropna=True)
    n_games = df["Name"].nunique()

    year_valid = df["Year"].dropna()
    year_min = int(year_valid.min()) if not year_valid.empty else None
    year_max = int(year_valid.max()) if not year_valid.empty else None

    overview = {
        "n_records": n_records,
        "n_cols": n_cols,
        "n_platforms": n_platforms,
        "n_genres": n_genres,
        "n_publishers": n_publishers,
        "n_games": n_games,
        "year_min": year_min,
        "year_max": year_max,
        "missing_summary": get_missing_summary(df).to_dict(orient="records"),
        "n_duplicates": 0,  # Đã loại bỏ ở bước preprocess; hiển thị để minh bạch
    }
    return overview


def get_describe_table(df: pd.DataFrame) -> list:
    """
    Thống kê mô tả (count, mean, std, min, quartiles, max) cho các biến số:
    Year và các cột doanh số. Dùng cho trang Tổng quan dữ liệu.
    """
    cols = ["Year"] + NUMERIC_SALES_COLS
    desc = df[cols].describe().T.round(3)
    desc.insert(0, "Biến", desc.index)
    desc = desc.rename(columns={"25%": "Q1", "50%": "Trung vị", "75%": "Q3"})
    return desc.to_dict(orient="records")
