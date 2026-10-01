"""
routes/dashboard.py
--------------------
Các route cho trang chủ (Index) và trang Tổng quan dữ liệu (Overview).
"""

from flask import Blueprint, render_template

from analysis.data_loader import get_dataframe
from analysis.preprocessing import get_dataset_overview, get_describe_table

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    """Trang chủ giới thiệu đề tài và điều hướng tới các trang phân tích."""
    return render_template("index.html")


@dashboard_bp.route("/overview")
def overview():
    """Trang mô tả bộ dữ liệu: số bản ghi, số thuộc tính, giá trị thiếu, v.v."""
    df = get_dataframe()
    overview_data = get_dataset_overview(df)
    describe_table = get_describe_table(df)
    sample_rows = df.head(10).to_dict(orient="records")
    columns = list(df.columns)
    return render_template(
        "overview.html",
        overview=overview_data,
        describe_table=describe_table,
        sample_rows=sample_rows,
        columns=columns,
    )
