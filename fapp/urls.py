from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'fapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('addpost/', views.addpost, name='addpost'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('upvote/<str:pk>', views.up_vote, name='upvote'),
    path('downvote/<str:pk>/', views.down_vote, name='downvote'),
    path('comments/post/<str:pk>', views.comment, name='comments'),
    path('profile/<str:pk>', views.show_user_profile, name='profile'),
    path('edit_profile/<str:pk>', views.edit_profile, name="edit_profile"),
    path('delete_account/<str:pk>', views.delete_account, name="delete_account"),
    path('delete_foodie/<str:pk>', views.delete_post, name='delete_foodie'),
    path('delete_comment/<str:pk>', views.delete_comment, name='delete_comment')
]