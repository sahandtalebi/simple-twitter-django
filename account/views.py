from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
# Create your views here.
from django.views import View
from account.forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

from account.models import Relation
from home.models import Post


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request.POST or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'با موفقیت انجام شد', 'success')
            return redirect('account:user_login')
        else:
            return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    templates_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('path')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request.POST or None)
        return render(request, self.templates_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت لاگین شدید', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'یوزرنیم یا پسورد اشتباه است', 'waring')

        return render(request, self.templates_name, {'form': form})


class UserLogout(LoginRequiredMixin, View):
    # login_url = 'account/login'

    def get(self, request):
        logout(request)
        messages.success(request, 'شما با موفقیت لاگ اوت شدید', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        posts = user.posts.all()
        return render(request, self.template_name, {'user': user, 'posts': posts, 'is_following': is_following})


class UserUpdateProfile(LoginRequiredMixin, View):
    template_name = 'account/update_profile.html'
    form_class = UserProfileUpdateForm

    def get(self, request, user_id):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            request.user.save()
            messages.success(request, 'پروفایل شما با موفقیت اپدیت شد', 'success')
        else:
            messages.error(request, 'پروفایل اپدیت نشد لطفا دوباره تلاش کنید', 'danger')
        return redirect('account:user_profile', request.user.id)


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'شما قبلا این کاربر را فالو کرده اید', 'danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, 'فالو انجام شد', 'success')
        return redirect('account:user_profile', user_id)


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'شما این کاربر را انفالو کردید', 'success')
        else:
            messages.error(request, 'شما کاربر را فالو نکردید', 'danger')
        return redirect('account:user_profile', user_id)


class UsersView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'account/users.html', {'users': users})
