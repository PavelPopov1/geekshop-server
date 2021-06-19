from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from users.models import User


# Create your views here.

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index')
def index(request):
    context = {'title': 'GeekShop - Админ'}
    return render(request, 'admins/admin.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index')
def admin_users(request):
    context = {'title': 'GeekShop - Админ - Все пользователи', 'users_obj': User.objects.all()}
    return render(request, 'admins/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index')
def admin_users_create(request):
    if request.method == "POST":
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно добавлен!")
            return HttpResponseRedirect(reverse('admins:admin_users'))
        else:
            print(form.errors)
    else:
        form = UserAdminRegistrationForm()
    context = {
        'title': 'GeekShop - Админ - Регистрация',
        'form': form
    }
    return render(request, 'admins/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index')
def admin_users_update(request, id):
    cur_user = User.objects.get(id=id)
    if request.method == "POST":
        form = UserAdminProfileForm(data=request.POST,
                               files=request.FILES,
                               instance=cur_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно обновлен!")
            return HttpResponseRedirect(reverse('admins:admin_users'))
        else:
            print(form.errors)
    else:
        form = UserAdminProfileForm(instance=cur_user)

    context = {'title': 'GeekShop - Админ - Обновление пользователя',
               'form': form,
               'cur_user': cur_user}
    return render(request, 'admins/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index')
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    messages.success(request, "Пользователь успешно удален!")
    return HttpResponseRedirect(reverse('admins:admin_users'))


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='index')
def admin_users_return(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    messages.success(request, "Пользователь успешно восстановлен!")
    return HttpResponseRedirect(reverse('admins:admin_users'))