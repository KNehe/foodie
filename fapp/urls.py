from django.urls import path
from . import views

app_name = 'fapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('addpost/', views.addpost, name='addpost'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout')
]