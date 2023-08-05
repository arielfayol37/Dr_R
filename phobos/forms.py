# forms.py

from django import forms
from .models import Course, Assignment, Question, McqAnswer, FloatAnswer, McqExpressionAnswer

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # TODO: Implement image upload. Make sure the image is uploaded to media/phobos/images/course_images
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

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'course', 'difficulty_level', 'due_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id':'assignment-name'}),
            'course': forms.Select(attrs={'class': 'form-control', 'id':'assignment-course'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control', 'id': 'difficulty-level'})
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
        model = McqExpressionAnswer
        fields = ['content']
