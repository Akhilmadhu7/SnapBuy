from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _



from . models import Customuser

# Register your models here.


class Customadmin(UserAdmin):
    
    fieldsets = (
        (None, {
            "fields": ('phone_number', 'email', 'username'
                
            ),
        }),

        (_('personal information'), {
            "fields": ('first_name','last_name',)
        }),

        (_('Permissions'), {
            "fields": ('is_active', 'is_superuser', 'groups', 'user_permissions')
        }),

        (_('Important dates'), {
            "fields": ('last_login', 'date_joined')
        })
    )

    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('phone_number', 'email', 'username',  'password1', 'password2')

            }),
    )

    list_display = (
        'phone_number', 'email', 'username', 'is_staff', 'is_active'
    )
    list_editable = ('is_active',)

    search_fields = (
        'phone_number', 'email', 'username'
    )

    ordering = ('username',)
    
    


admin.site.register(Customuser, Customadmin)