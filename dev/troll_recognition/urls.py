from django.urls import path
from .views import TrollPredictionView

urlpatterns = [
    path('predict/', TrollPredictionView.as_view(), name='troll_prediction')
]