from django.apps import AppConfig

class WebManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_management'

    def ready(self):
        import web_management.mqtt
        web_management.mqtt.start_mqtt_client()