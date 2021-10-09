from django.urls import path

from users.views import LoginView, RegisterView, LogoutView, profile, verify

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify')
]