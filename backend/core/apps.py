from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from core.plugins.registry import registry
        from core.domain import events

        registry.load_plugins()
        registry.sync_channels_to_db()

    
