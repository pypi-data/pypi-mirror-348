from django.apps import AppConfig


class pluginConfig(AppConfig):
    name = 'aa_proxy_reg'
    label = 'proxy_reg'
    
    def ready(self):
        # Импортируем хуки при загрузке приложения
        from . import hooks  # noqa