from django.urls import path
from . import views

app_name = 'users_auth'
urlpatterns = [
    path('users_auth/', views.user_home, name='user_home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]