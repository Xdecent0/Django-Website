# accounts/urls.py
from django.urls import path
from .views import SignUpView
from .views import UserProfileView

app_name = 'accounts'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
