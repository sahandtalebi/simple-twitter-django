from django.contrib import admin

# Register your models here.
from home.models import Post, Comment, Vote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('updated', )
    prepopulated_fields = {'slug': ('body',)}  # به صورت دیفالت فقط در ادمنی پنل حنگو
    raw_id_fields = ('user', )


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'post')
    list_filter = ('created', 'user')
    raw_id_fields = ('user', 'post', 'replay')


admin.site.register(Vote)