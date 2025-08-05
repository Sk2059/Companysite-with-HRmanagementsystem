# yourapp/forms.py

from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            'company_name',
            'company_type',
            'quote',
            'author_name',
            'author_position',
            'company_logo',
            'author_image',
            'is_active',
        ]
        widgets = {
            'quote': forms.Textarea(attrs={'rows': 4}),
        }
