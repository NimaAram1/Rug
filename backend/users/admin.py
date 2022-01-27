from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import UserCreateFormAdmin, UserChangeFormAdmin

# getting user model
User = get_user_model()

class UserAdmin(BaseAdmin):
    add_form = UserCreateFormAdmin
    form = UserChangeFormAdmin
    list_display = ["email", "username"]
    list_filter = ["is_admin"]
    fieldsets = (
        (None, {"fields":["email", "username"]}),
        ("اطلاعات بیشتر", {"fields":["name"]}),
        ("اطلاعات شخصی و دسترسی ها", {"fields":["password", "is_admin", "is_active"]})
    )
    add_fieldsets = (
        (None, {"fields":["email", "username", "name", "phone_number", "password", "repeated_password"]})
    )
    search_fields = ["email", "username"]
    ordering = ["username"]
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
