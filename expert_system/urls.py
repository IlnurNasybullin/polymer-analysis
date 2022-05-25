from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index),
    path('save', views.save),
    path('history', views.history),
    path('calculate', views.calculate),
    path('logout', views.logout_view)
]