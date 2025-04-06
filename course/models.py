from django.db import models
from model_utils.models import TimeStampedModel
    

# Create your models here.
class School(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Course(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    grade = models.PositiveIntegerField()
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'Course: {self.title}'


class Lesson(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    lesson_url = models.URLField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return f'Lesson: {self.title}'


class Assignment(TimeStampedModel):
    class Type(models.TextChoices):
        QUIZ = 'quiz', 'Quiz'
        CODE = 'code', 'Code'
        ESSAY = 'essay', 'Essay'

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assignment_type = models.CharField(max_length=10, choices=Type.choices)
    max_score = models.PositiveIntegerField()
    ai_autocheck = models.BooleanField(default=False)

    def __str__(self):
        return f'Assignment: {self.title}'


class Submission(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CHECKED = 'checked', 'Checked'
        REJECTED = 'rejected', 'Rejected'

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    answer_text = models.TextField(null=True, blank=True)
    code = models.TextField(null=True, blank=True)
    file_path = models.FileField(upload_to='submissions/', null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    checked_by_ai = models.BooleanField(default=False)
    feedback = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f'{self.assignment.title} by {self.student.full_name}'


class Recommendation(TimeStampedModel):
    class Source(models.TextChoices):
        AI = 'ai', 'AI'
        TEACHER = 'teacher', 'Teacher'

    student = models.ForeignKey('users.User', on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    text = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=10, choices=Source.choices)

    def __str__(self):
        return f"Rec. for {self.student.username} ({self.source})"


class ClassGroup(models.Model):
    name = models.CharField(max_length=20)  # e.g. "7A"
    teacher = models.ForeignKey('users.User', on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"Class {self.name}"


class ClassStudent(models.Model):
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, limit_choices_to={'role': 'student'})

    class Meta:
        unique_together = ('class_group', 'student')

    def __str__(self):
        return f"{self.student.username} in {self.class_group.name}"