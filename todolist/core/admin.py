from core.models import User

from django.contrib import admin


@admin.action(description='Reset password for default')
def reset_password(modeladmin, request, queryset):
    for user_ in queryset:
        user_.set_password(user_.default_password)
        user_.save()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fields = ('username', 'first_name', 'last_name', 'email', 'default_password', 'is_staff', 'is_active', 'date_joined', 'last_login')
    readonly_fields = ('date_joined', 'last_login')
    
    actions = [reset_password]


admin.site.register(User, UserAdmin)
