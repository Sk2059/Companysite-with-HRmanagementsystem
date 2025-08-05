from django.contrib import admin
from .models import Course
from .models import CourseRegistration


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'course_type', 'level', 'mode', 'duration', 'fee', 'is_active', 'start_date'
    )
    list_filter = ('level', 'course_type', 'mode', 'is_active')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ('-start_date',)


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course_type', 'duration', 'mode', 'submitted_at')
    search_fields = ('name', 'email', 'course_type')
    list_filter = ('course_type', 'duration', 'mode', 'batch')
