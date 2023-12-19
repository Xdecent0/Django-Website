# reservation/urls.py
from django.urls import path
from .views import home, MenuView, TableListView, AboutView, reserve_table, user_profile, select_table, register, logout_view, user_confirm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    # path('tables/', TableListView.as_view(), name='table_list'),
    path('user_confirm/', user_confirm, name='user_confirm'),
    path('about/', AboutView.as_view(), name='about'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('reserve/', select_table, name='select_table'),
    path('reserve/<int:table_id>/', reserve_table, name='reserve_table'),
    path('profile/', user_profile, name='profile'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', success_url='/reservation/profile/'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
