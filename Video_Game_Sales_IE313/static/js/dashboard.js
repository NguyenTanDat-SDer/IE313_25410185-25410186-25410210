// dashboard.js
// Bổ sung một số hiệu ứng nhỏ cho giao diện Dashboard.
// Toàn bộ dữ liệu và biểu đồ được tạo phía server bằng Pandas/Seaborn;
// tệp này chỉ xử lý phần trải nghiệm giao diện phía client.

document.addEventListener("DOMContentLoaded", function () {
    // Phóng to ảnh biểu đồ khi click (mở tab mới) để xem chi tiết
    document.querySelectorAll(".chart-img").forEach(function (img) {
        img.style.cursor = "zoom-in";
        img.addEventListener("click", function () {
            window.open(img.src, "_blank");
        });
    });

    // Đánh dấu mục điều hướng hiện tại (dự phòng nếu class active chưa được set)
    var path = window.location.pathname;
    document.querySelectorAll(".sidebar-nav a").forEach(function (link) {
        if (link.getAttribute("href") === path) {
            link.classList.add("active");
        }
    });
});
