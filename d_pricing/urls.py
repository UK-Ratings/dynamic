from django.contrib import admin
from django.urls import path, include
import debug_toolbar
#from base.views import custom_500_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('base.urls')),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler500 = custom_500_error