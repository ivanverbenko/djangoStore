from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
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


class UserProfileView(LoginRequiredMixin, CommonMixin, UpdateView):
    model = User
    form_class = UsersProfileForm
    template_name = 'users/profile.html'
    title = 'Профиль'

    def get_object(self, queryset=None):
        user_profile = get_object_or_404(User, pk=self.request.user.pk)
        return user_profile

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))