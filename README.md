# Dự án Quản lý Danh sách Công việc với Socket
# Tổng quan
Dự án này là một ứng dụng quản lý danh sách công việc (To-do List) đơn giản, sử dụng socket để giao tiếp giữa client và server, kết hợp với giao diện người dùng đồ họa (GUI) được xây dựng bằng PyQt5. Ứng dụng cho phép người dùng thực hiện các thao tác tạo, đọc, cập nhật và xóa (CRUD) các công việc, được lưu trữ trong cơ sở dữ liệu SQLite. Server và client chạy đồng thời, với client gửi yêu cầu đến server qua socket.
Tính năng

# Server (Socket):
Xử lý các yêu cầu CRUD từ client:
Lấy danh sách tất cả công việc.
Tạo công việc mới.
Lấy thông tin chi tiết của một công việc theo ID.
Cập nhật một công việc cụ thể.
Xóa một công việc cụ thể.




# Giao diện người dùng (GUI):
Hiển thị danh sách công việc.
Cung cấp biểu mẫu để thêm hoặc chỉnh sửa công việc (tiêu đề và mô tả).
Bao gồm các nút để thêm, cập nhật và xóa công việc.
Tự động làm mới danh sách công việc sau khi có thay đổi.


# Cơ sở dữ liệu: Sử dụng SQLite để lưu trữ công việc một cách bền vững.
Chạy đồng thời: Chạy server socket và GUI PyQt5 cùng lúc bằng cách sử dụng threading.



# Kiến thức cần thiết
Socket Programming: Quen thuộc với lập trình socket trong Python, bao gồm server-client communication và JSON serialization.
PyQt5: Kiến thức về cách tạo ứng dụng GUI, bố cục, widget và xử lý sự kiện.
Threading: Kiến thức cơ bản về chạy nhiều tiến trình đồng thời trong Python.

# Hướng dẫn cài đặt


Cài đặt các thư viện phụ thuộc:
pip install -r requirements.txt

Lệnh này sẽ cài đặt PyQt5 như được liệt kê trong requirements.txt.

Chạy ứng dụng:
python main.py


Server socket sẽ khởi động tại 127.0.0.1:12345.
Giao diện PyQt5 sẽ mở trong một cửa sổ mới.



Hướng dẫn sử dụng

Giao diện người dùng (GUI):

Bảng bên trái hiển thị danh sách công việc (ID và tiêu đề).
Nhấp vào một công việc để xem chi tiết ở bảng bên phải.
Sử dụng bảng bên phải để:
Nhập tiêu đề và mô tả, sau đó nhấn "Add Todo" để tạo công việc mới.
Chọn một công việc, chỉnh sửa chi tiết và nhấn "Update Todo" để lưu thay đổi.
Chọn một công việc và nhấn "Delete Todo" để xóa.


Thông báo lỗi sẽ xuất hiện nếu thao tác thất bại (ví dụ: không chọn công việc).


Server:

Server chạy trên 127.0.0.1:12345 và xử lý các yêu cầu từ client qua socket.
Các yêu cầu được gửi dưới dạng JSON với các hành động: get_all, create, get, update, delete.



# Lưu ý

Cơ sở dữ liệu SQLite (todos.db) được tạo tự động trong thư mục dự án khi ứng dụng khởi động.
Server chạy trên cổng 12345.
GUI sử dụng socket để giao tiếp với server, vì vậy server phải đang chạy để GUI hoạt động bình thường.
Ứng dụng sử dụng threading để chạy server socket và GUI PyQt5 đồng thời. Server chạy trong một luồng daemon để đảm bảo nó kết thúc khi GUI đóng.

# Giấy phép
Dự án này được tạo với mục đích học tập và không được cấp phép để sử dụng trong môi trường sản xuất.
