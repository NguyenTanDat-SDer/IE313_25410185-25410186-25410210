"""
routes/analysis.py
-------------------
Các route cho 4 trang phân tích thăm dò dữ liệu (EDA):
  - /time-analysis      : Phân tích theo thời gian (4.1, 4.2)
  - /genre-analysis     : Phân tích theo thể loại (4.3, 4.4)
  - /platform-analysis  : Phân tích theo nền tảng (4.5)
  - /region-analysis    : Phân tích theo khu vực + Top games (4.6, 4.7, 4.8)
"""

from flask import Blueprint, render_template

from analysis.data_loader import get_dataframe
from analysis.analysis import (
    analyze_games_per_year,
    analyze_global_sales_per_year,
    analyze_genre_sales,
    analyze_genre_average_sales,
    analyze_platform_sales,
    analyze_genre_region_heatmap,
    analyze_region_sales_over_time,
    analyze_top_games,
)

analysis_bp = Blueprint("analysis", __name__)



@analysis_bp.route("/region-analysis")
def region_analysis():
    """4.6, 4.7, 4.8: Heatmap khu vực-thể loại, doanh số khu vực theo thời gian, Top games."""
    df = get_dataframe()
    genre_region_heatmap = analyze_genre_region_heatmap(df)
    region_sales_over_time = analyze_region_sales_over_time(df)
    top_games = analyze_top_games(df)
    return render_template(
        "region_analysis.html",
        genre_region_heatmap=genre_region_heatmap,
        region_sales_over_time=region_sales_over_time,
        top_games=top_games,
    )