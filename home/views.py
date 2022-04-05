from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from account.models import Relation
from home.forms import UpdateAndCreatePostForm, CommentCreateForm, CommentReplaysForm, SearchForm
from home.models import Post, Comment, Vote
from django.contrib import messages


class HomeView(View):
    form_class = SearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/home.html', {'posts': posts, 'form': self.form_class})


class DetailView(View):
    template_name = 'home/detail.html'
    form_class_comment = CommentCreateForm
    form_class_replays = CommentReplaysForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id):
        user_can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            user_can_like = True
        form = self.form_class_comment
        reply_form = self.form_class_replays
        comments = self.post_instance.pcomments.filter(is_replay=False)
        return render(request, self.template_name,
                      {'post': self.post_instance, 'comments': comments, 'form': form, 'reply_form': reply_form,
                       'user_can_like': user_can_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class_comment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'کامنت شما با موفقیت ارسال شد', 'success')
            return redirect('home:post_detail', self.post_instance.id)
        else:
            messages.error('request', 'کامنت شما ارسال نشد لطفا دوباره تلاش کنید', 'danger')
            return redirect('home:post_detail', self.post_instance.id)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'پست با موفقبت پاک شد', 'success')
        else:
            messages.error(request, 'شما نمیتواند پست را پاک کنید', 'error')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = UpdateAndCreatePostForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.post_instance.user.id == request.user.id:
            messages.error(request, 'شما نمیتوانید این پست را اپدیت کنید', 'error')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.post_instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.post_instance)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'با موفقیت اپدیت  شد', 'success')
            return redirect('home:post_detail', self.post_instance.id)


class PostCreateView(LoginRequiredMixin, View):
    form_class = UpdateAndCreatePostForm
    template_name = 'home/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'پست با موفقیت ارسال شد', 'success')
            return redirect('home:post_detail', new_post.id)
        messages.error(request, 'شما نمیتوانید پست اضافه کنید')


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplaysForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST or None)
        if form.is_valid():
            replay = form.save(commit=False)
            replay.user = request.user
            replay.post = post
            replay.replay = comment
            replay.is_replay = True
            replay.save()
            messages.success(request, 'کامنت شما ارسال شد', 'success')
        else:
            messages.error(request, 'کامنت ارسال نشد دوباره تلاش کنید', '')

        return redirect('home:post_detail', post.id)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post)
        if like.exists():
            messages.error(request, 'شما قبلا این پست را لایک کرده اید', 'danger')
        else:
            Vote.objects.create(user=request.user, post=post)
            messages.success(request, 'پست با موفقیت لایک شد', 'success')

        return redirect('home:post_detail', post.id)


class ExploreView(LoginRequiredMixin, View):

    def get(self, request):
        followers = list(Relation.objects.filter(from_user=request.user).values_list('to_user', flat=True))
        posts = Post.objects.filter(user__in=followers)

        return render(request, 'home/explore.html', {'posts': posts})
