from django.apps import AppConfig


class TheListConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "the_list"

    def ready(self):
        import the_list.signals
