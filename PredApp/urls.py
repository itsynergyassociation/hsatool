from django.urls import path
from .views import Predictions, home, History, Settings


app_name = 'PredApp'

urlpatterns = [
    path('', home, name='home'),
    path('prediction', Predictions.as_view(), name='prediction'),
    path('history', History.as_view(), name='history'),
    path('settings', Settings.as_view(), name='settings'),
]