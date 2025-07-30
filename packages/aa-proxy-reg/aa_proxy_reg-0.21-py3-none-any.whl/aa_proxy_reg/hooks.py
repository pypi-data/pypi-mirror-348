from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.utils.translation import gettext_lazy as _
from . import urls

class ProxyRegMenuItem(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(
            self,
            'Починить чаты Eve Online',  # Текст в меню
            'fas fa-comments',  # Иконка Font Awesome (например, fa-rocket)
            'aa_proxy_reg:main',  # Имя URL из urls.py
            navactive=['aa_proxy_reg:'],  # Подсветка меню при активности
        )


@hooks.register('menu_item_hook')  # Регистрация хука
def register_menu():
  return ProxyRegMenuItem()

@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "aa_proxy_reg", r"^aa_proxy_reg/")

# class SettingsMenuItem(MenuItemHook):
#     def __init__(self):
#         super().__init__(
#             'Настройки плагина',
#             'fas fa-cog',
#             'aa_proxy_reg:settings',
#             navactive=['aa_proxy_reg:settings'],
#         )

# @hooks.register('menu_item_hook')
# def register_menu():
#     return SettingsMenuItem()