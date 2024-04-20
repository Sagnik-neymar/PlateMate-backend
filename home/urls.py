from django.urls import path, include
from home import views


urlpatterns = [
    path("", views.index, name='index'),
    path("result", views.result, name='result'),

    path("visual", views.visual, name='visual'),
    path("prediction", views.prediction, name='prediction'),
]