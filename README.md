"# agv_3" 
***khởi động dự án : 
- tạo môi trường ảo
- tải các gói về bằng cú pháp pip install -r requirements.txt
- rồi chạy bằng cú pháp: uvicorn web_management.asgi:application --host 127.0.0.1 --port 8000 --lifespan off
- set biến môi trường trước khi chạy server : set DJANGO_SETTINGS_MODULE=web_management.settings

***đổi tên app :
   UPDATE django_content_type SET app_label = 'new_app_name' WHERE app_label = 'old_app_name';
   UPDATE django_migrations SET app = 'new_app_name' WHERE app = 'old_app_name';


***test api cho agv_identify :
{
         "agv_id": 1,
         "maximum_speed": 100,
         "parking_lot": 1,
         "battery_capacity": 1000,
         "maximum_load": 500,
         "guidance_type": "line_following",
         "load_transfer": "Automatic",
         "operation": true,
         "connection": true
     }

***test api cho material_management :
     {
         "material_name": "Steel",
         "material_unit": "KG",
         "material_weight": 1000
     }

7A14020014031E7832000A000F025828A0015B7F
7A1401000A012328FF00050008042C30D400897F
7A1403001E02201C64000F001203E83A9800F27F
7A140400280419284B0014001905DC4B00012C7F
7A14050032012580780019001E07D05DC001A37F

7A09020001141F40020101017F

***cách xóa dữ liệu trong bảng agv_management_agv_data của database:
- Mở pgAdmin 4 và chọn database
- Mở query tool
- Xóa toàn bộ dữ liệu trong bảng và đặt lại giá trị của một cột id (là khóa chính) về 1 trong PostgreSQL sau khi xóa toàn bộ dữ liệu của bảng:

TRUNCATE TABLE ten_bang RESTART IDENTITY;

- Để tối ưu hóa dung lượng và giúp database hoạt động trơn tru hơn, chạy lệnh VACUUM trên bảng đã xóa, đảm bảo dung lượng được giải phóng trong database :

VACUUM ten_bang;

*** cách giải phóng các cổng đang được kết nối:
- Xem các cổng đang được kết nối: 

netstat -ano | findstr :5173

- Kết thúc tiến trình sử dụng cổng: 

taskkill /PID <PID> /F
