"""
analysis.py
------------
Các hàm phân tích thăm dò dữ liệu (EDA) và trực quan hóa cho đề tài
"Phân tích thăm dò dữ liệu trò chơi điện tử (Video Game Sales) bằng
thư viện Seaborn".

Mỗi hàm vẽ biểu đồ sẽ:
  1. Tính toán dữ liệu tổng hợp cần thiết bằng Pandas.
  2. Vẽ biểu đồ bằng Seaborn/Matplotlib.
  3. Lưu hình ảnh vào static/images/ dưới dạng PNG.
  4. Trả về dữ liệu tổng hợp (dùng để hiển thị bảng số liệu trên Dashboard).

Các bản ghi thiếu Year chỉ bị loại trừ cục bộ trong các phân tích theo
thời gian (4.1, 4.2, 4.7), đúng như mô tả trong báo cáo; các phân tích
khác (Genre, Platform, Top Games) sử dụng toàn bộ dữ liệu hợp lệ.
"""

import os

import matplotlib

matplotlib.use("Agg")  # Không cần giao diện đồ họa khi chạy trên server Flask

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")

IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static",
    "images",
)
os.makedirs(IMAGES_DIR, exist_ok=True)

REGION_COLS = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
REGION_LABELS = {
    "NA_Sales": "Bắc Mỹ",
    "EU_Sales": "Châu Âu",
    "JP_Sales": "Nhật Bản",
    "Other_Sales": "Khu vực khác",
}


def _save_fig(fig, filename: str) -> str:
    """Lưu figure vào static/images và trả về đường dẫn tương đối cho template."""
    path = os.path.join(IMAGES_DIR, filename)
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return f"images/{filename}"


# ---------------------------------------------------------------------------
# 4.1. Số lượng trò chơi theo năm
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 4.2. Tổng doanh số toàn cầu theo năm
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 4.3. Tổng doanh số theo thể loại (Genre)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 4.4. Doanh số trung bình theo thể loại
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 4.5. Top 10 nền tảng theo tổng doanh số toàn cầu
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 4.6. Heatmap doanh số theo thể loại và khu vực
# ---------------------------------------------------------------------------
def analyze_genre_region_heatmap(df: pd.DataFrame):
    pivot = df.groupby("Genre")[REGION_COLS].sum()
    pivot = pivot.rename(columns=REGION_LABELS)
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(8, 7))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax, cbar_kws={"label": "Doanh số (triệu bản)"})
    ax.set_title("Heatmap doanh số theo thể loại và khu vực")
    ax.set_xlabel("Khu vực")
    ax.set_ylabel("Thể loại")
    img_path = _save_fig(fig, "fig6_genre_region_heatmap.png")

    table = pivot.round(2).reset_index().to_dict(orient="records")

    return {
        "image": img_path,
        "table": table,
        "columns": ["Genre"] + list(REGION_LABELS.values()),
    }


# ---------------------------------------------------------------------------
# 4.7. Doanh số các khu vực theo thời gian
# ---------------------------------------------------------------------------
def analyze_region_sales_over_time(df: pd.DataFrame):
    data = df.dropna(subset=["Year"]).copy()
    data["Year"] = data["Year"].astype(int)
    region_by_year = data.groupby("Year")[REGION_COLS].sum().reset_index()

    melted = region_by_year.melt(
        id_vars="Year", var_name="Khu vực", value_name="Doanh số"
    )
    melted["Khu vực"] = melted["Khu vực"].map(REGION_LABELS)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    sns.lineplot(data=melted, x="Year", y="Doanh số", hue="Khu vực", marker="o", ax=ax)
    ax.set_title("Doanh số theo khu vực qua các năm")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Doanh số (triệu bản)")
    ax.tick_params(axis="x", rotation=90)
    ax.legend(title="Khu vực")
    img_path = _save_fig(fig, "fig7_region_year.png")

    return {
        "image": img_path,
        "table": region_by_year.round(2).to_dict(orient="records"),
    }


# ---------------------------------------------------------------------------
# 4.8. Top 10 trò chơi theo doanh số toàn cầu
# ---------------------------------------------------------------------------
def analyze_top_games(df: pd.DataFrame, top_n: int = 10):
    top_games = (
        df[["Name", "Platform", "Year", "Genre", "Global_Sales"]]
        .sort_values("Global_Sales", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top_games, x="Global_Sales", y="Name", color="#DD8452", ax=ax
    )
    ax.set_title(f"Top {top_n} trò chơi theo doanh số toàn cầu")
    ax.set_xlabel("Doanh số toàn cầu (triệu bản)")
    ax.set_ylabel("Trò chơi")
    img_path = _save_fig(fig, "fig8_top_games.png")

    top_row = top_games.iloc[0]

    return {
        "image": img_path,
        "table": top_games.round(2).to_dict(orient="records"),
        "top_name": top_row["Name"],
        "top_value": round(float(top_row["Global_Sales"]), 2),
    }


def run_all_analysis(df: pd.DataFrame) -> dict:
    """Chạy toàn bộ 8 phân tích và trả về dict kết quả, dùng cho trang Overview."""
    return {
        # "games_per_year": analyze_games_per_year(df),
        # "global_sales_per_year": analyze_global_sales_per_year(df),
        # "genre_sales": analyze_genre_sales(df),
        # "genre_average_sales": analyze_genre_average_sales(df),
        # "platform_sales": analyze_platform_sales(df),
        "genre_region_heatmap": analyze_genre_region_heatmap(df),
        "region_sales_over_time": analyze_region_sales_over_time(df),
        "top_games": analyze_top_games(df),
    }