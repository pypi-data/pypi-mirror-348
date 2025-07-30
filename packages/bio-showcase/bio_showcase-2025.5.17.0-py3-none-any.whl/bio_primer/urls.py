from django.urls import path

from . import views

app_name = "primer"

urlpatterns = [
    # ex: /primer/
    path('', views.IndexView.as_view(), name='index'),
    path('design/', views.design, name='design'),
]
