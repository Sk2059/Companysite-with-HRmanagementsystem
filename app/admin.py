from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'company_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author_name', 'company_name', 'quote')