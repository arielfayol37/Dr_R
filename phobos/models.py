from django.db import models
from django.contrib.auth.models import User
#from django.contrib.postgres.fields import ArrayField

class Course(models.Model):
    """
    Course class to store course on the platform.
    
    There are no standalone courses .i.e Each course
    has an instructor or multiple instructors.

    The name doesn't have to be unique, given that
    different instructors/instutions may give a course
    with the same title.

    # TODO: the subject should not be a text field in the html template,
            given that there are already known subjects like 
            Computer Science, Maths, Or Physics. So Subject 
            should be drop-down list.
            Same applies to difficulty level.
    
    """
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    DIFFICULT = 'DIFFICULT'
    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (DIFFICULT, 'Difficult'),
    ]
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    number_of_students = models.IntegerField()
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    professors = models.ManyToManyField('Professor')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Course {self.name}, difficulty level - {self.difficulty_level}"

class Professor(User):
    """
    Class to store professors on the platform.
    """
    department = models.CharField(max_length=50)

class Assignment(models.Model):
    """
    Assignments in the form of quizzes/homeworks will be created by
    professors and may be comprised of one or multiple questions. 
    """
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    #questions = models.ManyToManyField('Question')
    timestamp = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f"Assigment {self.name} for '{self.course.name.title()}'"

class Question(models.Model):
    """
    A question may be standalone or attributed to a Assigment. 
    
    A question may be comprised of a sub question like a, b, c, or d.
    (Optional: the sub questions themselves may have i, ii, iii, iv, like Twitter threads).

    A question may be a multiple choice question (and single-answer or multiple-answers type)
    OR an expression question with answers that may be numeric or algebraic expressions.

    A question may have randomized variables associated to it. Such that different students
    will have different variables and hence different answers. 

    The weight attribute is used to compute a student's grade for an Assignment.
    So all the questions in an assignment may have the same weight (uniform distribution),
    or different weights based on the instructor's input or automated (based on difficulty)
    
    # TODO: !Important 
        Though the category input from the instructor at the time of creation of the question
        will be optional, we may use embeddings to determine the similarity with other questions 
        and assign the same category as the closest question.

        The vector or matrix representation of the question should be computed at the time of
        creation or later(automatically - it may also be updated as more questions come in).
        That will be used for category assignment described above, and most importantly for
        the search engine.

    """
    text = models.TextField(null=False, blank=False)
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE, related_name="questions")
    category = models.CharField(max_length=50, null=True, blank=True)
    topic = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    weight = models.FloatField()
    sub_questions = models.ManyToManyField('self', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question {self.number} for {self.assigment}"
    


class QuestionImage(models.Model):
    """
    Class for images associated with a particular question.
    For example, for more description or for a multiple choice question where the options
    are images.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='phobos/images/question_images/', blank=True, null=True)

class Hint(models.Model):
    """
    Each question/subquestion may have hints in the form of text or urls to help.
    """
    text = models.TextField(blank=False, null=False) # Professor must include text(description)
    url = models.URLField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='hints', on_delete=models.CASCADE)

    def __str__(self):
        return f"Hint {self.id} for {self.question}"

class McqAnswer(models.Model):
    """
    The answer(s) to a multiple choice question may be an image or a text or both. 
    # TODO: Make sure user inputs either or both. So during testing, make sure the
    # the view as well as the front end takes care of that.

    # TODO: (maybe) Change the related names to 'answers'.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_answers')
    image = models.ImageField(upload_to='phobos/images/question_images/', \
                              blank=True, null=True)
    content = models.CharField(blank=True, null=True, max_length=200)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Answer for {self.question}: {self.content[:50]}"
        else:
            return f"Incorrect MCQ Answer for {self.question}: {self.content[:50]}"
        
class FloatAnswer(models.Model):
    """
    Answer to a structural question may be an algebraic expression, a vector, or a float.
    # TODO: (maybe) Change related name to 'answers'S.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="float_answers")
    content = models.FloatField(blank=False, null=False)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        if self.is_answer:
            return f"Correct Float Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect Float Answer for {self.question}: {self.content}"

class ExpressionAnswer(models.Model):
    """
    An expression for a structural question may just be interpreted as text. The math.js library
    will parse the expression given by the teacher and the resulting text will be stored.
    When a user will input an answer, it will be compared to that text.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="expression_answers")
    content = models.CharField(max_length=100) 
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        if self.is_answer:
            return f"Correct Expression Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect Expression Answer for {self.question}: {self.content}"
    

class VectorAnswer(models.Model):
    """
    A vector answer for a structural question can be n-dimensional. n >= 2  
    """
    # TODO: !Important This is GPT 3.5 Implementation:
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='vector_answers')
    content = models.FloatField(blank=False, null=False)  # Store the vector as an array of floats
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        if self.is_answer:
            return f"Correct Vector Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect Vector Answer for {self.question}: {self.content}"

    