from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from users.models import User


# Create your views here.

class AdminIndexView(ListView):
    model = User
    template_name = 'admins/admin.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminIndexView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminIndexView, self).dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ - Все пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Пользователь успешно добавлен!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ - Регистрация'
        return context

    def get_success_url(self):
        referer_url = self.request.META.get('HTTP_REFERER')  # get the referer url from request's 'META' dictionary
        return referer_url  # return referer url for redirection

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Пользователь успешно обновлен!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ - Обновление пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Пользователь успешно удален!'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


class UserReturnView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')
    success_message = 'Пользователь успешно восстановлен!'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserReturnView, self).dispatch(request, *args, **kwargs)