from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import ConfirmationCode
from .serializers import StudentRegistrationSerializer

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('student_id', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'role')
    fieldsets = (
        (None, {'fields': ('student_id', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_id', 'email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    
admin.site.register(User, UserAdmin)
admin.site.register(ConfirmationCode)
