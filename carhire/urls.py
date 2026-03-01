# carhire/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import index_view # Import your index view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. FIX THE ROOT PATH: Assign the home page
    path('', index_view, name='index'), 
    
    # 2. KEEP YOUR PREFIXED PATHS
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('fleet/', include('fleet.urls', namespace='fleet')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('payments/', include('payments.urls', namespace='payments')),
]

# 3. SAFETY: Ensure static is only handled at the VERY end
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)