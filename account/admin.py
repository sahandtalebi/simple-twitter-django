from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from django.contrib.auth.models import User

from account.models import Relation, Profile

admin.register(Relation)


class ProfileAdmin(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileAdmin, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)