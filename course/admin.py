# course/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg
from .models import (
    School, Course, Lesson, Assignment, Submission,
    Recommendation, ClassGroup, ClassStudent
)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'address')
    list_filter = ('city', 'region')
    search_fields = ('name', 'city', 'region', 'address')
    ordering = ('name',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            teacher_count=Count('teacherprofile', distinct=True),
            student_count=Count('studentprofile', distinct=True)
        )
        return queryset
    
    def teacher_count(self, obj):
        return obj.teacher_count
    teacher_count.admin_order_field = 'teacher_count'
    teacher_count.short_description = 'Teachers'
    
    def student_count(self, obj):
        return obj.student_count
    student_count.admin_order_field = 'student_count'
    student_count.short_description = 'Students'


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'lesson_url')
    ordering = ('order',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'created_by', 'created', 'lesson_count')
    list_filter = ('grade', 'created_by')
    search_fields = ('title', 'description')
    date_hierarchy = 'created'
    inlines = [LessonInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            lesson_count=Count('lesson', distinct=True)
        )
        return queryset
    
    def lesson_count(self, obj):
        return obj.lesson_count
    lesson_count.admin_order_field = 'lesson_count'
    lesson_count.short_description = 'Lessons'


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1
    fields = ('title', 'assignment_type', 'max_score', 'ai_autocheck')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'assignment_count', 'view_course_link')
    list_filter = ('course__title', 'course__grade')
    search_fields = ('title', 'content')
    ordering = ('course', 'order')
    inlines = [AssignmentInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            assignment_count=Count('assignment', distinct=True)
        )
        return queryset
        
    def assignment_count(self, obj):
        return obj.assignment_count
    assignment_count.admin_order_field = 'assignment_count'
    assignment_count.short_description = 'Assignments'
    
    def view_course_link(self, obj):
        url = reverse("admin:course_course_change", args=[obj.course.id])
        return format_html('<a href="{}">View Course</a>', url)
    view_course_link.short_description = 'Course Details'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'assignment_type', 'max_score', 'ai_autocheck', 'submission_count', 'avg_score')
    list_filter = ('assignment_type', 'ai_autocheck', 'lesson__course')
    search_fields = ('title', 'description')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            submission_count=Count('submission', distinct=True),
            avg_score=Avg('submission__score')
        )
        return queryset
    
    def submission_count(self, obj):
        return obj.submission_count
    submission_count.admin_order_field = 'submission_count'
    submission_count.short_description = 'Submissions'
    
    def avg_score(self, obj):
        if obj.avg_score is None:
            return "N/A"
        return f"{obj.avg_score:.2f}"
    avg_score.admin_order_field = 'avg_score'
    avg_score.short_description = 'Average Score'


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'score', 'checked_by_ai', 'created')
    list_filter = ('status', 'checked_by_ai', 'assignment__assignment_type')
    search_fields = ('student__username', 'student__full_name', 'assignment__title')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'modified')
    
    fieldsets = (
        ('Submission Info', {
            'fields': ('assignment', 'student', 'status', 'score')
        }),
        ('Content', {
            'fields': ('answer_text', 'code', 'file_path')
        }),
        ('Feedback', {
            'fields': ('checked_by_ai', 'feedback')
        }),
        ('Metadata', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('student', 'source', 'generated_at', 'text_preview')
    list_filter = ('source', 'generated_at')
    search_fields = ('student__username', 'student__full_name', 'text')
    date_hierarchy = 'generated_at'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Preview'


class ClassStudentInline(admin.TabularInline):
    model = ClassStudent
    extra = 1
    raw_id_fields = ('student',)


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'student_count')
    list_filter = ('teacher',)
    search_fields = ('name', 'teacher__username', 'teacher__full_name')
    inlines = [ClassStudentInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            student_count=Count('classstudent', distinct=True)
        )
        return queryset
    
    def student_count(self, obj):
        return obj.student_count
    student_count.admin_order_field = 'student_count'
    student_count.short_description = 'Students'


@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_group')
    list_filter = ('class_group',)
    search_fields = ('student__username', 'student__full_name', 'class_group__name')
    raw_id_fields = ('student', 'class_group')
