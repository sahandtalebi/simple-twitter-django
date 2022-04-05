from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),

    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/update/<int:user_id>', views.UserUpdateProfile.as_view(), name='user_update'),

    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnFollowView.as_view(), name='user_unfollow'),

    path('users/', views.UsersView.as_view(), name='user_all'),
]
