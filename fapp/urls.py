from django.urls import path
from . import views

app_name = 'fapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('addpost/', views.addpost, name='addpost')
]