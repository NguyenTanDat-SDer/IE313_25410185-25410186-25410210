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

