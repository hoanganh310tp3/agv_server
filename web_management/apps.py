from django.apps import AppConfig
from django.db.models.signals import post_migrate
import logging
import threading
import time

logger = logging.getLogger(__name__)

# def run_scheduler():
#     from requests_management.schedule import create_schedule, schedule_agv
#     try:
#         # Đợi 5 giây để đảm bảo database và các service khác đã sẵn sàng
#         time.sleep(5)
        
#         # Tạo và lưu lịch vào database
#         create_schedule()
#         logger.info("Schedule created and saved to database successfully")
        
#         # Chạy scheduler để điều phối AGV
#         schedule_agv()
#         logger.info("AGV scheduler started successfully")
#     except Exception as e:
#         logger.error(f"Failed to create and start schedule: {e}")

class WebManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_management'
    # scheduler_started = False

    def ready(self):
        import web_management.mqtt
        web_management.mqtt.start_mqtt_client()
        
        # # Chỉ chạy scheduler một lần
        # if not self.scheduler_started:
        #     self.scheduler_started = True
        #     # Chạy scheduler trong thread riêng
        #     scheduler_thread = threading.Thread(target=run_scheduler)
        #     scheduler_thread.daemon = True  # Thread sẽ tắt khi main thread tắt
        #     scheduler_thread.start()