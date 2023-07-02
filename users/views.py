
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from common.views import CommonMixin
from products.models import Basket
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UsersProfileForm
from django.contrib import auth

# Create your views here.
def login(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form' : form,'title':'Логин'}
    return render(request,'users/login.html',context)

class UserRegistrationView(CommonMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    title = 'Регистрация'


class UserProfileView(CommonMixin,UpdateView):
    model = User
    form_class = UsersProfileForm
    template_name = 'users/profile.html'
    title = 'Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))