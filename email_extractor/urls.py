from django.urls import include, path

urlpatterns = [
    path('extractor/', include('extractor.urls')),
]
