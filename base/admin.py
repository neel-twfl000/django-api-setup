from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account

from .forms import UserCreationForm, UserChangeForm

user_fields = ('first_name', 'last_name', 'email',  'password')

personal_fields = ( 'phone', 'last_login', 'is_active', 'is_staff', 'is_superuser')

class AccountAdmin(BaseUserAdmin):

    form = UserChangeForm

    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'phone', 'is_staff',  'is_superuser')

    list_filter = ('is_superuser',)

    fieldsets = (

        (None, {'fields': user_fields}),

       

        ('Personal info', {'fields': personal_fields}),

    )

    add_fieldsets = (

        (None, {'fields': user_fields}),

       

        ('Personal info', {'fields': personal_fields}),

    )

    search_fields = ('email', 'first_name', 'phone')

    ordering = ('email',)

    filter_horizontal = ()

admin.site.register(Account, AccountAdmin)
