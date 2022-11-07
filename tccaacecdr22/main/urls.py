from django.urls import path
from main import views

urlpatterns = [
    path('', views.indexpage, name='index'),
    path('index', views.indexpage, name='index'),
    path('results', views.results, name='results'),
    path('error', views.results, name='error'),
    path('sobre', views.sobrepage, name='sobre'),
]