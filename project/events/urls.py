from django.urls import path

from .views import EventDetailAPIView, EventApproveAPIView, EventUnApproveListAPIView, EventListOrCreateAPIView

urlpatterns = [
    path('', EventListOrCreateAPIView.as_view(), name='list_or_create_events'),
    path('<int:pk>/', EventDetailAPIView.as_view(), name='details_event'),
    path('unapproved/', EventUnApproveListAPIView.as_view(), name='list_unapproved_events'),
    path('approve/<int:pk>/', EventApproveAPIView.as_view(), name='approve_event'),
]