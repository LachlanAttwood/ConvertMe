from django.urls import path
from PPT_to_PDF import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.myView, name='PPT_to_PDF'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)