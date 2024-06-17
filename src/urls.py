from django.conf.urls import handler404
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/', include('inventory.urls')),
    path('api/v1/', include('user.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
