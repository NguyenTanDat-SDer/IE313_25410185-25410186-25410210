"""
data_loader.py
---------------
Chịu trách nhiệm đọc dữ liệu thô từ tệp vgsales.csv.
Tách riêng bước đọc dữ liệu khỏi bước tiền xử lý và phân tích
để dễ bảo trì và kiểm thử.
"""

import os
from functools import lru_cache

import pandas as pd

# Đường dẫn mặc định tới tệp dữ liệu (data/vgsales.csv)
DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "vgsales.csv",
)

def load_raw_data(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """
    Đọc dữ liệu thô từ tệp CSV.

    Parameters
    ----------
    path : str
        Đường dẫn tới tệp vgsales.csv.

    Returns
    -------
    pd.DataFrame
        DataFrame chứa dữ liệu thô, chưa qua xử lý.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy tệp dữ liệu tại: {path}")

    df = pd.read_csv(path)
    return df


@lru_cache(maxsize=1)
def _load_and_preprocess_cached(path: str):
    """Đọc và tiền xử lý dữ liệu một lần duy nhất, cache kết quả cho cả ứng dụng."""
    # Import cục bộ để tránh vòng lặp import giữa data_loader và preprocessing
    from analysis.preprocessing import preprocess_data

    raw_df = load_raw_data(path)
    return preprocess_data(raw_df)


def get_dataframe(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """
    Trả về DataFrame đã được tiền xử lý, dùng chung cho toàn bộ các route.
    Dữ liệu chỉ được đọc và xử lý một lần (cache) để tránh đọc lại CSV
    mỗi khi người dùng chuyển trang trên Dashboard.
    """
    return _load_and_preprocess_cached(path).copy()