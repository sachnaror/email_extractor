from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('download/txt/', views.download_as_txt, name='download_txt'),
    path('download/csv/', views.download_as_csv, name='download_csv'),
    path('download/xls/', views.download_as_xls, name='download_xls'),
]
