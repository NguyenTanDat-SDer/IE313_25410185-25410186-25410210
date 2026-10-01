"""
app.py
------
Điểm khởi chạy chính của ứng dụng Flask Web Dashboard cho đề tài
"Phân tích thăm dò dữ liệu trò chơi điện tử (Video Game Sales) bằng
thư viện Seaborn" - IE313.

Chạy ứng dụng:
    python app.py

Mặc định ứng dụng chạy tại http://127.0.0.1:5000
"""

from flask import Flask

from routes.dashboard import dashboard_bp
from routes.analysis import analysis_bp


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analysis_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
