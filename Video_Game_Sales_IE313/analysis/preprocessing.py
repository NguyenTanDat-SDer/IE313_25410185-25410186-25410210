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


