"# agv_3" 
khởi động dự án : 
- tạo môi trường ảo
- tải các gói về bằng cú pháp pip install -r requirements.txt
- rồi chạy bằng cú pháp: uvicorn web_management.asgi:application --host 127.0.0.1 --port 8000 --lifespan off
set DJANGO_SETTINGS_MODULE=web_management.settings

đổi tên app :
   UPDATE django_content_type SET app_label = 'new_app_name' WHERE app_label = 'old_app_name';
   UPDATE django_migrations SET app = 'new_app_name' WHERE app = 'old_app_name';


test api cho agv_identify :
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

test api cho material_management :
     {
         "material_name": "Steel",
         "material_unit": "KG",
         "material_weight": 1000
     }

7A14020014031E7832000A000F025828A0015B7F
7A1401000A012328FF00050008042C30D400897F
7A 14 03 00 1E 02 20 1C 64 00 0F 00 12 03 E8 3A 98 00 F2 7F
7A 14 04 00 28 04 19 28 4B 00 14 00 19 05 DC 4B 00 01 2C 7F
7A 14 05 00 32 01 25 80 78 00 19 00 1E 07 D0 5D C0 01 A3 7F