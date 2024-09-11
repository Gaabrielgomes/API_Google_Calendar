from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_events, name='get_all_events'),
    path('new-event/', views.create_event, name='new-event'),
    path('update-event/', views.update_event, name='update-event'),
    path('delete-event/', views.delete_event, name='delete-event'),
]