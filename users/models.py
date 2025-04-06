from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=10, choices=Role.choices)
    full_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile')
    grade = models.IntegerField()
    school = models.ForeignKey('course.School', on_delete=models.SET_NULL, null=True)
    parent_contact = models.CharField(max_length=255)

    def __str__(self):
        return f'Student: {self.user.full_name}'


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=100, default='Информатика')
    school = models.ForeignKey('course.School', on_delete=models.SET_NULL, null=True)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f'Teacher: {self.user.full_name}'

