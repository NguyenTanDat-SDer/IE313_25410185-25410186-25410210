"""
routes/analysis.py
-------------------
Các route cho 4 trang phân tích thăm dò dữ liệu (EDA):
  - /time-analysis      : Phân tích theo thời gian (4.1, 4.2)
  - /genre-analysis     : Phân tích theo thể loại (4.3, 4.4)
  - /platform-analysis  : Phân tích theo nền tảng (4.5)
  - /region-analysis    : Phân tích theo khu vực + Top games (4.7, 4.8, 4.9)
  - /publisher-analysis : Top 10 nhà phát hành (4.6)
  - /distribution-analysis : Phân phối doanh số (4.10)
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
    analyze_region_totals,
    analyze_top_publishers,
    analyze_sales_distribution,
    analyze_platform_distribution,
    analyze_region_distribution,
)

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/time-analysis")
def time_analysis():
    """4.1 và 4.2: Số lượng trò chơi theo năm và tổng doanh số toàn cầu theo năm."""
    df = get_dataframe()
    games_per_year = analyze_games_per_year(df)
    global_sales_per_year = analyze_global_sales_per_year(df)
    return render_template(
        "time_analysis.html",
        games_per_year=games_per_year,
        global_sales_per_year=global_sales_per_year,
    )


@analysis_bp.route("/genre-analysis")
def genre_analysis():
    """4.3 và 4.4: Tổng doanh số và doanh số trung bình theo thể loại."""
    df = get_dataframe()
    genre_sales = analyze_genre_sales(df)
    genre_average_sales = analyze_genre_average_sales(df)
    return render_template(
        "genre_analysis.html",
        genre_sales=genre_sales,
        genre_average_sales=genre_average_sales,
    )


@analysis_bp.route("/platform-analysis")
def platform_analysis():
    """4.5: Top 10 nền tảng theo tổng doanh số toàn cầu."""
    df = get_dataframe()
    platform_sales = analyze_platform_sales(df)
    platform_distribution = analyze_platform_distribution(df)
    return render_template(
        "platform_analysis.html",
        platform_sales=platform_sales,
        platform_distribution=platform_distribution,
    )


@analysis_bp.route("/region-analysis")
def region_analysis():
    """4.6, 4.7, 4.8: Heatmap khu vực-thể loại, doanh số khu vực theo thời gian, Top games."""
    df = get_dataframe()
    genre_region_heatmap = analyze_genre_region_heatmap(df)
    region_sales_over_time = analyze_region_sales_over_time(df)
    top_games = analyze_top_games(df)
    region_totals = analyze_region_totals(df)
    region_distribution = analyze_region_distribution(df)
    return render_template(
        "region_analysis.html",
        region_distribution=region_distribution,
        region_totals=region_totals,
        genre_region_heatmap=genre_region_heatmap,
        region_sales_over_time=region_sales_over_time,
        top_games=top_games,
    )


@analysis_bp.route("/publisher-analysis")
def publisher_analysis():
    """4.6: Top 10 nhà phát hành theo tổng doanh số toàn cầu."""
    df = get_dataframe()
    top_publishers = analyze_top_publishers(df)
    return render_template("publisher_analysis.html", top_publishers=top_publishers)


@analysis_bp.route("/distribution-analysis")
def distribution_analysis():
    """4.10: Phân phối Global_Sales (histplot) và boxplot theo thể loại."""
    df = get_dataframe()
    dist = analyze_sales_distribution(df)
    return render_template("distribution_analysis.html", dist=dist)
