# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import StudentProfile, TeacherProfile, User

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = 'Teacher Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'full_name', 'role', 'email']
    search_fields = ('name', 'email')



@admin.register(TeacherProfile)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user__id', 'user__first_name', 'user__role']
    search_fields = ['user__full_name']
    raw_id_fields = ('user',)


@admin.register(StudentProfile)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user__id', 'user__first_name', 'user__role']
    raw_id_fields = ('user',)
