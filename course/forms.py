from django import forms
from .models import Course
from .models import CourseRegistration

class CourseForm(forms.ModelForm):
    syllabus_json = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        help_text="Syllabus data in JSON format"
    )
    
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'syllabus': forms.HiddenInput(),
        }
    
    def clean_syllabus_json(self):
        import json
        syllabus_data = self.cleaned_data.get('syllabus_json', '[]')
        if syllabus_data:
            try:
                return json.loads(syllabus_data)
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid syllabus format")
        return []
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        syllabus_data = self.cleaned_data.get('syllabus_json', [])
        if syllabus_data:
            instance.syllabus = syllabus_data
        if commit:
            instance.save()
        return instance


class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistration
        fields = '__all__'
        widgets = {
            'skills': forms.HiddenInput(),
            'expectations': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 3}),
        }
