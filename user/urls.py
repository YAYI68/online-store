
from django.urls import path
from user.views import logout, UserRegistrationView, LoginView

urlpatterns = [
    path('signup', UserRegistrationView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', logout),
]
