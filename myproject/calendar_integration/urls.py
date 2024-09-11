from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_events, name='get_all_events'),
    path('event/<str:id>/', views.get_event_by_id, name='get-event-by-id'),
    path('events/<str:start>|<str:end>/', views.get_events_by_period, name='get-events-by-period'),
    path('events/<str:summary>/', views.get_events_by_summary, name='get-events-by-summary'),
    path('new-event/', views.create_event, name='new-event'),
    path('update-event/', views.update_event, name='update-event'),
    path('delete-event/', views.delete_event, name='delete-event'),
]