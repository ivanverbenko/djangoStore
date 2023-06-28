from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from products.views import *
from users.views import login, registration, profile, logout

app_name='users'
urlpatterns = [
    path('login/',login,name='login'),
    path('registration/',registration,name='registration'),
    path('profile/',profile,name='profile'),
    path('logout', logout, name='logout')
]
