from django.urls import path
from . import views

app_name = 'aa_proxy_reg'

urlpatterns = [
    path('', views.main_view, name='main'),
    path('call_api/', views.call_api_endpoint, name='call_api')
]