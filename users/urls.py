from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from products.views import *
from users.views import login, logout, UserRegistrationView, UserProfileView, EmailVerificationView
from django.contrib.auth.decorators import login_required
app_name='users'
urlpatterns = [
    path('login/',login,name='login'),
    path('registration/',UserRegistrationView.as_view(),name='registration'),
    path('profile/',login_required(UserProfileView.as_view()),name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<uuid:code>', EmailVerificationView.as_view(), name='verification')
]
#branch test