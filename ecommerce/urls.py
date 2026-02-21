from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <-- 1. Import settings
from django.conf.urls.static import static  # <-- 2. Import static file server

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    # <-- 3. Add this magic line to the end!
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
