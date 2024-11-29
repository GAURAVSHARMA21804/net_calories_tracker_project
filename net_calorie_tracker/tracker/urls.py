from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('users_dashboard/', views.user_dashboard, name='users_dashboard'),
    path('admin_panel_dashboard/', views.admin_dashboard, name='admin_panel_dashboard'),
    path('search_food/', views.search_food, name='search_food'),
    path('save_food_log/', views.save_food_log, name='save_food_log'),
    path('search_activity/', views.search_activity, name='search_activity'),
    path('save_activity_log/', views.save_activity_log, name='save_activity_log'),
]
