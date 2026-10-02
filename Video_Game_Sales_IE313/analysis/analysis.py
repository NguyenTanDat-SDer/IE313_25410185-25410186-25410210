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
def analyze_games_per_year(df: pd.DataFrame):
    data = df.dropna(subset=["Year"]).copy()
    data["Year"] = data["Year"].astype(int)
    counts = data.groupby("Year").size().reset_index(name="Số lượng trò chơi")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=counts, x="Year", y="Số lượng trò chơi", color="#4C72B0", ax=ax)
    ax.set_title("Số lượng trò chơi phát hành theo năm")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Số lượng trò chơi")
    ax.tick_params(axis="x", rotation=90)
    img_path = _save_fig(fig, "fig1_year_game_count.png")

    peak_year = int(counts.loc[counts["Số lượng trò chơi"].idxmax(), "Year"])
    peak_value = int(counts["Số lượng trò chơi"].max())

    return {
        "image": img_path,
        "table": counts.to_dict(orient="records"),
        "peak_year": peak_year,
        "peak_value": peak_value,
    }


# ---------------------------------------------------------------------------
# 4.2. Tổng doanh số toàn cầu theo năm
# ---------------------------------------------------------------------------
def analyze_global_sales_per_year(df: pd.DataFrame):
    data = df.dropna(subset=["Year"]).copy()
    data["Year"] = data["Year"].astype(int)
    sales_by_year = (
        data.groupby("Year")["Global_Sales"].sum().reset_index(name="Global_Sales")
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        data=sales_by_year, x="Year", y="Global_Sales", marker="o", color="#C44E52", ax=ax
    )
    ax.set_title("Tổng doanh số toàn cầu (Global Sales) theo năm")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Tổng doanh số (triệu bản)")
    ax.tick_params(axis="x", rotation=90)
    img_path = _save_fig(fig, "fig2_year_global_sales.png")

    peak_row = sales_by_year.loc[sales_by_year["Global_Sales"].idxmax()]

    return {
        "image": img_path,
        "table": sales_by_year.round(2).to_dict(orient="records"),
        "peak_year": int(peak_row["Year"]),
        "peak_value": round(float(peak_row["Global_Sales"]), 2),
    }


# ---------------------------------------------------------------------------
# 4.3. Tổng doanh số theo thể loại (Genre)
# ---------------------------------------------------------------------------
def analyze_genre_summary(df: pd.DataFrame) -> list:
    """Bảng tổng hợp theo thể loại: tổng, số game, trung bình, trung vị (Global_Sales)."""
    summary = (
        df.groupby("Genre")["Global_Sales"]
        .agg(Tong="sum", So_game="count", Trung_binh="mean", Trung_vi="median")
        .sort_values("Tong", ascending=False)
        .round(3)
        .reset_index()
    )
    return summary.to_dict(orient="records")


def analyze_genre_sales(df: pd.DataFrame):
    genre_sales = (
        df.groupby("Genre")["Global_Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=genre_sales, x="Global_Sales", y="Genre", color="#55A868", ax=ax
    )
    ax.set_title("Tổng doanh số toàn cầu theo thể loại (Genre)")
    ax.set_xlabel("Tổng doanh số (triệu bản)")
    ax.set_ylabel("Thể loại")
    img_path = _save_fig(fig, "fig3_genre_sales.png")

    return {
        "image": img_path,
        "table": genre_sales.round(2).to_dict(orient="records"),
        "summary_table": analyze_genre_summary(df),
        "top_genre": genre_sales.iloc[0]["Genre"],
        "top_value": round(float(genre_sales.iloc[0]["Global_Sales"]), 2),
        "bottom_genre": genre_sales.iloc[-1]["Genre"],
        "bottom_value": round(float(genre_sales.iloc[-1]["Global_Sales"]), 2),
    }


# ---------------------------------------------------------------------------
# 4.4. Doanh số trung bình theo thể loại
# ---------------------------------------------------------------------------
def analyze_genre_average_sales(df: pd.DataFrame):
    genre_avg = (
        df.groupby("Genre")["Global_Sales"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    genre_avg.columns = ["Genre", "Avg_Global_Sales"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=genre_avg, x="Avg_Global_Sales", y="Genre", color="#8172B2", ax=ax
    )
    ax.set_title("Doanh số toàn cầu trung bình trên mỗi trò chơi theo thể loại")
    ax.set_xlabel("Doanh số trung bình (triệu bản/trò chơi)")
    ax.set_ylabel("Thể loại")
    img_path = _save_fig(fig, "fig4_genre_average_sales.png")

    return {
        "image": img_path,
        "table": genre_avg.round(3).to_dict(orient="records"),
        "top_genre": genre_avg.iloc[0]["Genre"],
        "top_value": round(float(genre_avg.iloc[0]["Avg_Global_Sales"]), 3),
    }


# ---------------------------------------------------------------------------
# 4.5. Top 10 nền tảng theo tổng doanh số toàn cầu
# ---------------------------------------------------------------------------
def analyze_platform_sales(df: pd.DataFrame, top_n: int = 10):
    platform_sales = (
        df.groupby("Platform")["Global_Sales"]
        .agg(Global_Sales="sum", So_game="count", Trung_binh="mean")
        .sort_values("Global_Sales", ascending=False)
        .head(top_n)
        .round(3)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=platform_sales, x="Global_Sales", y="Platform", color="#CCB974", ax=ax
    )
    ax.set_title(f"Top {top_n} nền tảng theo tổng doanh số toàn cầu")
    ax.set_xlabel("Tổng doanh số (triệu bản)")
    ax.set_ylabel("Nền tảng")
    img_path = _save_fig(fig, "fig5_platform_sales.png")

    return {
        "image": img_path,
        "table": platform_sales.round(2).to_dict(orient="records"),
        "top_platform": platform_sales.iloc[0]["Platform"],
        "top_value": round(float(platform_sales.iloc[0]["Global_Sales"]), 2),
    }


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

    share = pivot.div(pivot.sum(axis=1), axis=0) * 100
    share_table = share.round(1).reset_index().to_dict(orient="records")

    return {
        "image": img_path,
        "table": table,
        "share_table": share_table,
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


# ---------------------------------------------------------------------------
# Bảng tổng doanh số theo khu vực (dùng cho mục 4.7)
# ---------------------------------------------------------------------------
def analyze_region_totals(df: pd.DataFrame):
    totals = df[REGION_COLS].sum()
    total_all = totals.sum()
    rows = [
        {
            "Khu vực": REGION_LABELS[c],
            "Tổng doanh số": round(float(totals[c]), 1),
            "Tỷ trọng (%)": round(float(totals[c] / total_all * 100), 1),
        }
        for c in REGION_COLS
    ]
    return {"table": rows}


# ---------------------------------------------------------------------------
# Top 10 nhà phát hành theo tổng doanh số toàn cầu
# ---------------------------------------------------------------------------
def analyze_top_publishers(df: pd.DataFrame, top_n: int = 10):
    data = df.dropna(subset=["Publisher"])
    pub = (
        data.groupby("Publisher")["Global_Sales"]
        .agg(Global_Sales="sum", So_game="count", Trung_binh="mean")
        .sort_values("Global_Sales", ascending=False)
        .head(top_n)
        .round(2)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=pub, x="Global_Sales", y="Publisher", color="#64B5CD", ax=ax)
    ax.set_title(f"Top {top_n} nhà phát hành theo tổng doanh số toàn cầu")
    ax.set_xlabel("Tổng doanh số (triệu bản)")
    ax.set_ylabel("Nhà phát hành")
    img_path = _save_fig(fig, "fig11_top_publishers.png")

    total = float(df["Global_Sales"].sum())
    return {
        "image": img_path,
        "table": pub.to_dict(orient="records"),
        "top_publisher": pub.iloc[0]["Publisher"],
        "top_value": round(float(pub.iloc[0]["Global_Sales"]), 2),
        "top_share": round(float(pub.iloc[0]["Global_Sales"]) / total * 100, 1),
    }


# ---------------------------------------------------------------------------
# Phân phối Global_Sales: histplot + boxplot theo thể loại
# ---------------------------------------------------------------------------
def analyze_sales_distribution(df: pd.DataFrame):
    g = df["Global_Sales"]

    # Histogram (trục x log để nhìn rõ đuôi phân phối lệch phải)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(g, bins=60, log_scale=True, color="#4C72B0", ax=ax)
    ax.axvline(g.median(), color="#C44E52", linestyle="--", label=f"Trung vị = {g.median():.2f}")
    ax.axvline(g.mean(), color="#55A868", linestyle="--", label=f"Trung bình = {g.mean():.2f}")
    ax.set_title("Phân phối doanh số toàn cầu của mỗi trò chơi (trục log)")
    ax.set_xlabel("Global_Sales (triệu bản, thang log)")
    ax.set_ylabel("Số lượng trò chơi")
    ax.legend()
    hist_path = _save_fig(fig, "fig9_sales_distribution.png")

    # Boxplot theo thể loại
    order = df.groupby("Genre")["Global_Sales"].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="Global_Sales", y="Genre", order=order, ax=ax, fliersize=2)
    ax.set_xscale("log")
    ax.set_title("Phân phối Global_Sales theo thể loại (trục log)")
    ax.set_xlabel("Global_Sales (triệu bản, thang log)")
    ax.set_ylabel("Thể loại")
    box_path = _save_fig(fig, "fig10_genre_boxplot.png")

    total = float(g.sum())
    n = len(g)
    stats = {
        "count": int(n),
        "mean": round(float(g.mean()), 3),
        "std": round(float(g.std()), 3),
        "min": round(float(g.min()), 2),
        "q25": round(float(g.quantile(0.25)), 2),
        "median": round(float(g.median()), 2),
        "q75": round(float(g.quantile(0.75)), 2),
        "p90": round(float(g.quantile(0.90)), 2),
        "p99": round(float(g.quantile(0.99)), 2),
        "max": round(float(g.max()), 2),
        "skew": round(float(g.skew()), 2),
        "pct_ge_1m": round(float((g >= 1).mean() * 100), 2),
        "pct_lt_05m": round(float((g < 0.5).mean() * 100), 2),
        "top1pct_share": round(float(g.nlargest(int(n * 0.01)).sum() / total * 100), 2),
    }
    return {"hist_image": hist_path, "box_image": box_path, "stats": stats}


# ---------------------------------------------------------------------------
# Phân phối Global_Sales theo nền tảng (Top 10) - boxplot
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# Phân phối doanh số theo khu vực - violinplot (chỉ các game có doanh số > 0)
# ---------------------------------------------------------------------------
def analyze_region_distribution(df: pd.DataFrame):
    import numpy as np

    rows = []
    frames = []
    for col in REGION_COLS:
        x = df[col]
        nz = x[x > 0]
        rows.append(
            {
                "Khu vực": REGION_LABELS[col],
                "Ty_le_0": round(float((x == 0).mean() * 100), 1),
                "So_game_co_doanh_so": int(len(nz)),
                "Trung_vi": round(float(nz.median()), 3),
                "Trung_binh": round(float(nz.mean()), 3),
                "P90": round(float(nz.quantile(0.9)), 3),
            }
        )
        frames.append(
            pd.DataFrame(
                {"Khu vực": REGION_LABELS[col], "log10_sales": np.log10(nz.values)}
            )
        )
    long_df = pd.concat(frames, ignore_index=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(
        data=long_df, x="Khu vực", y="log10_sales", inner="quartile", cut=0, ax=ax
    )
    ticks = [-2, -1, 0, 1]
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{10 ** t:g}" for t in ticks])
    ax.set_title("Phân phối doanh số theo khu vực (chỉ game có doanh số > 0, thang log)")
    ax.set_xlabel("Khu vực")
    ax.set_ylabel("Doanh số (triệu bản, thang log)")
    img_path = _save_fig(fig, "fig13_region_violin.png")

    return {"image": img_path, "table": rows}


def run_all_analysis(df: pd.DataFrame) -> dict:
    """Chạy toàn bộ các phân tích và trả về dict kết quả, dùng cho trang Overview."""
    return {
        "games_per_year": analyze_games_per_year(df),
        "global_sales_per_year": analyze_global_sales_per_year(df),
        "genre_sales": analyze_genre_sales(df),
        "genre_average_sales": analyze_genre_average_sales(df),
        "platform_sales": analyze_platform_sales(df),
        "genre_region_heatmap": analyze_genre_region_heatmap(df),
        "region_sales_over_time": analyze_region_sales_over_time(df),
        "top_games": analyze_top_games(df),
        "region_totals": analyze_region_totals(df),
        "top_publishers": analyze_top_publishers(df),
        "sales_distribution": analyze_sales_distribution(df),
        "platform_distribution": analyze_platform_distribution(df),
        "region_distribution": analyze_region_distribution(df),
    }
