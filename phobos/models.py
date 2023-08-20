from django.db import models
from django.contrib.auth.models import User
#from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

class DifficultyChoices(models.TextChoices):
    EASY = 'EASY', 'Easy'
    MEDIUM = 'MEDIUM', 'Medium'
    DIFFICULT = 'DIFFICULT', 'Difficult'

class SubjectChoices(models.TextChoices):    

    COMPUTER_SCIENCE = 'COMPUTER_SCIENCE', 'Computer Science'
    MATHS = 'MATHS', 'Maths'
    PHYSICS = 'PHYSICS', 'Physics'
    # TODO: Add more subject choices as needed.

class QuestionChoices(models.TextChoices):
    STRUCTURAL_EXPRESSION = 'STRUCTURAL_EXPRESSION', 'Structural Expression'
    STRUCTURAL_FLOAT = 'STRUCTURAL_FLOAT', 'Structural Float'
    STRUCTURAL_TEXT = 'STRUCTURAL_TEXT', 'Structural Text'
    STRUCTURAL_LATEX = 'STRUCTURAL_LATEX', 'Structural Latex'
    MCQ_EXPRESSION = 'MCQ_EXPRESSION', 'MCQ Expression'
    MCQ_FLOAT = 'MCQ_FLOAT', 'MCQ Float'
    MCQ_LATEX = 'MCQ_LATEX', 'MCQ Latex'
    MCQ_TEXT = 'MCQ_TEXT', 'MCQ Text'
    SURVEY = 'SURVEY', 'Survey'

class AssignmentChoices(models.TextChoices):
    QUIZ = 'QUIZ', 'Quiz'
    HOMEWORK = 'HOMEWORK', 'Homework'
    PRACTICE_TEST = 'PRACTICE_TEST', 'Practice Test'

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

    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=400, default="No description")
    subject = models.CharField(max_length=100,
                                choices=SubjectChoices.choices,
                                default=SubjectChoices.PHYSICS)
    number_of_students = models.IntegerField(blank=True, null=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )
    professors = models.ManyToManyField('Professor', related_name='courses')
    topics = models.ManyToManyField('Topic', related_name='courses')
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='phobos/images/course_covers', blank=True, null=True)

    def __str__(self):
        return f" Course {self.name}, difficulty level - {self.difficulty_level}"

class Professor(User):
    """
    Class to store professors on the platform.
    """
    department = models.CharField(max_length=50)

class Topic(models.Model):

    """
    A course may cover various topics. For example Mechanics and Fields in Physics, but should likely cover at most 3. 
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SubTopic(models.Model):
    """
    A topic may be comprised of various topics.
    For example, Faraday's law is a subtopic of electromagnetism.
    """
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name='sub_topics')
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Assignment(models.Model):
    """
    Assignments in the form of quizzes/homeworks/practice_test will be created by
    professors and may be comprised of one or multiple questions. 
    """
    name = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    timestamp = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    assigned_date = models.DateTimeField(blank=True, null=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )
    category = models.CharField(max_length=25, choices=AssignmentChoices.choices,
                                 default = AssignmentChoices.HOMEWORK)
    def __str__(self):
        return f"Assigment {self.name} ranked {self.difficulty_level} for '{self.course.name.title()}'"

class Question(models.Model):
    """
    A question may be standalone or attributed to a `Assigment`. 
    
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

    # Define choices for the topic 

    """

 
    number = models.CharField(blank=False, null=False, max_length=5)
    text = models.TextField(max_length= 2000, null=False, blank=False)
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE, \
                                   related_name="questions")
    category = models.CharField(max_length=50, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL, null=True, blank=True)
    num_points = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(15)]) # Add lower and upper bound.
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, \
                                        blank=True, related_name='sub_questions')
    timestamp = models.DateTimeField(auto_now_add=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.MEDIUM,
    )
    answer_type = models.CharField(
        max_length = 30,
        choices = QuestionChoices.choices,
        default = QuestionChoices.STRUCTURAL_TEXT
    )
    max_num_attempts = models.IntegerField(default=5)
    answer = models.CharField(max_length=1000, null=True, blank=True) # TODO: delete this attribute.
    deduct_per_attempt = models.FloatField(default=0.05, blank=True, null=True)
    margin_error = models.FloatField(default=0.03, blank=True, null=True)

    def __str__(self):
        return f"Question {self.number} ranked {self.difficulty_level} for {self.assignment}"
    


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

        
class FloatAnswer(models.Model):
    """
    Answer to a `structural Question` may be an algebraic expression, a vector, or a float.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="float_answers")
    content = models.FloatField(blank=False, null=False)

    def __str__(self):
            
        return f"Float Answer for {self.question}: {self.content}"
        
            
class ExpressionAnswer(models.Model):
    """
    An expression for a `structural Question` may just be interpreted as text. The math.js library
    will parse the expression given by the teacher and the resulting text will be stored.
    When a user will input an answer, it will be compared to that text.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="expression_answers")
    content = models.CharField(max_length=200) 
    
    def __str__(self):
        
        return f"Expression Answer for {self.question}: {self.content}"

class LatexAnswer(models.Model):
    """
    An answer may a latex string that will later be rendered in the JavaScript.
    For now, this is only used for MCQ `Questions`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='latex_answers')
    content = models.CharField(max_length=400)

    def __str__(self):

        return f"Latex Answer for {self.question}: {self.content}"
    
class TextAnswer(models.Model):
    """
    Probably less common, but a `Question` may have a text answer.
    Will implement semantic validation for text answers using a transformer later.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='text_answers')
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"Text Answer for {self.question}: {self.content}"

class MCQFloatAnswer(models.Model):
    """
    Answer to a `structural Question` may be an algebraic expression, a vector, or a float.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="mcq_float_answers")
    content = models.FloatField(blank=False, null=False)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Float Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Float Answer for {self.question}: {self.content}" 
        
            
class MCQExpressionAnswer(models.Model):
    """
    An expression for a `structural Question` may just be interpreted as text. The math.js library
    will parse the expression given by the teacher and the resulting text will be stored.
    When a user will input an answer, it will be compared to that text.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="mcq_expression_answers")
    content = models.CharField(max_length=200) 
    is_answer = models.BooleanField(default=False)
    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Expression Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Expression Answer for {self.question}: {self.content}" 

class MCQLatexAnswer(models.Model):
    """
    Latex answer for `MCQ Question`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_latex_answers')
    content = models.CharField(max_length=400)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Latex Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Latex Answer for {self.question}: {self.content}" 
    
class MCQTextAnswer(models.Model):
    """
    Text answer for `MCQ Question`.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_text_answers')
    content = models.CharField(max_length=400)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        if self.is_answer:
            return f"Correct MCQ Text Answer for {self.question}: {self.content}"
        else:
            return f"Incorrect MCQ Text Answer for {self.question}: {self.content}"    
    
class MCQImageAnswer(models.Model):
    """
    An answer to an `MCQ Question` may simply be an image.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='mcq_image_answers')
    image = models.ImageField(upload_to='phobos/images/question_images/', \
                              blank=True, null=True)   
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"Image answer for {self.quesiton} with url {self.image.url}" 

class VectorAnswer(models.Model):
    # !Important: Deprecated
    """
    A vector answer for a structural question can be n-dimensional. n >= 2  
    # TODO: !Important: the content should be an array of floats.
            We may not have to do this, since the vectors are usually going to 2D or 3D.
            As such, we can use one input field for each dimension.
    """
    

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='vector_answers')
    content = models.FloatField(blank=False, null=False)  # Store the vector as an array of floats

    def __str__(self):
        return f"Correct Vector Answer for {self.question}: {self.content}"
