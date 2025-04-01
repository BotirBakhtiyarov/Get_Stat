from django.urls import path
from . import views
from .views import DataReceiverView

urlpatterns = [
    path('api/data', DataReceiverView.as_view(), name='data-receiver'),
    path('api/stats', views.StatsView.as_view()),
]