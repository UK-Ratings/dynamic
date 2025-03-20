#from django.contrib import admin
from django.urls import path
from . import views
#from django.urls import include
#from django.contrib.auth import views as auth_views
#from .views import PasswordsChangeView
#from django.conf import settings
#from django.conf.urls.static import static


urlpatterns = [
    path('', views.base_home, name='base-home'),

#    path('trigger-500/', views.trigger_500_error, name='trigger-500'),
#    path('record-500/', views.custom_500_error, name='custom-500'),

]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#handler500 = 'base.views.custom_500_error'
