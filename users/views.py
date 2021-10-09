from django.shortcuts import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.shortcuts import render

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm
from users.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context

    def post(self, request, *args, **kwargs):
        if self.form_class(data=request.POST).is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username,
                                     password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return super(LoginView, self).post(request, *args, **kwargs)
        else:
            return super(LoginView, self).post(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно!'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            if send_verify_link(user):
                messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.success_url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Регистрация'
        return context


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    context = {
        'title': 'GeekShop - Профиле',
        'form': form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)


'''class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile_default')
    success_message = 'Данные сохранены!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Личный кабинет'
        context['basket'] = Basket.objects.filter(user=self.request.user)
        context['profile_form'] = UserProfileEditForm(data=self.request.POST, instance=self.request.user.userprofile)
        return context

    def get_success_url(self):
        referer_url = self.request.META.get('HTTP_REFERER')
        return referer_url  # return referer url for redirection

    def post(self, request, *args, **kwargs):
        super(ProfileView, self).post(request, *args, **kwargs)
        form = self.get_form(self.form_class)
        return self.form_valid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        profile_form = UserProfileEditForm(data=self.request.POST, instance=self.request.user.userprofile)
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile_form'] = profile_form

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
        return HttpResponseRedirect(self.success_url + f'{user.id}/')'''


class LogoutView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'products/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LogoutView, self).get_context_data(**kwargs)
        auth.logout(self.request)
        return context


def send_verify_link(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
    message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    #try:
    user = User.objects.get(email=email)
    if user and user.activation_key == activation_key and not user.is_activation_key_expired():
        user.activation_key = ''
        user.activation_key_expires = None
        user.is_active = True
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    return render(request, 'users/verification.html')
    #except Exception as e:
       # return HttpResponseRedirect(reverse('index'))


