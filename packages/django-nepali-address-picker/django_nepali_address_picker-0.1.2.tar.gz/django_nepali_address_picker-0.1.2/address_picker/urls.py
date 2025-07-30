from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.address_picker, name='address_picker'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-local-bodies/', views.load_local_bodies, name='ajax_load_local_bodies'),
] 