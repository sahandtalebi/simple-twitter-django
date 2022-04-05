from django.urls import path, re_path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:post_id>/', DetailView.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>', PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>', PostUpdateView.as_view(), name='post_update'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('replay/<int:post_id>/<int:comment_id>/', PostAddReplyView.as_view(), name='add_replay'),
    path('like/<int:post_id>/', PostLikeView.as_view(), name='post_like'),

    path('explore/', ExploreView.as_view(), name='post-explore')
]
