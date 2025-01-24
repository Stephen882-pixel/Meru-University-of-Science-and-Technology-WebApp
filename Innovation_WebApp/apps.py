from django.apps import AppConfig


class InnovationWebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Innovation_WebApp'


    def ready(self):
        import Innovation_WebApp.models
        
