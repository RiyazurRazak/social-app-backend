from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserFollowing
from .forms import RegistrationForm, UserEditForm


class AccountAdmin(UserAdmin):
    add_form = RegistrationForm
    form = UserEditForm
    model = Account
    list_display = ('username', 'email', 'fullname', 'is_admin', 'is_superuser', 'last_login')
    search_fields = ('username', 'email', 'fullname')
    readonly_fields = ('id', 'date_joined', 'last_login', 'email')
    filter_horizontal = ()
    filter_vertical = ()
    list_filter = ()
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2'), }),)
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal info', {'fields': ['fullname', 'avatar']}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(UserFollowing)
