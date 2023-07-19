# forms.py
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image', 'name', 'subject', 'difficulty_level','description', 'professors']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'course-name'}),
            'subject': forms.Select(attrs={'class': 'form-control', 'id': 'course-subject'}),
            # 'number_of_students': forms.NumberInput(attrs={'class': 'form-control', 'id': 'students-count'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control', 'id': 'difficulty-level'}),
            # TODO: the oninput is to a function to be defined in the JS file
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'course-description', 'oninput':"resizeTextarea(this)"}),
            'professors': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'course-professors'}),
        }