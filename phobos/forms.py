# forms.py

from django import forms
from .models import Course, Question, McqAnswer, FloatAnswer, ExpressionAnswer

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # TODO: Implement image upload. Make sure the image is uploaded to static/phobos/images/course_images
        fields = ['image', 'name', 'subject', 'difficulty_level','description','topics','professors']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'course-name'}),
            'subject': forms.Select(attrs={'class': 'form-control', 'id': 'course-subject'}),
            # 'number_of_students': forms.NumberInput(attrs={'class': 'form-control', 'id': 'students-count'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control', 'id': 'difficulty-level'}),
            # TODO: the oninput is to a function to be defined in the JS file
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'course-description',\
                                                  'style':"height: 30px" ,\
                                                    'oninput':"resizeTextarea(this)"}),
            'topics': forms.SelectMultiple(attrs={'class': 'form-control', 'id':'course-topics'}),
            'professors': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'course-professors'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'topic', 'sub_topic', 'num_points', 'parent_question']

class McqAnswerForm(forms.ModelForm):
    class Meta:
        model = McqAnswer
        fields = ['content','image', 'is_answer']

class FloatAnswerForm(forms.ModelForm):
    class Meta:
        model = FloatAnswer
        fields = ['content']

class ExpressionAnswerForm(forms.ModelForm):
    class Meta:
        model = ExpressionAnswer
        fields = ['content']
