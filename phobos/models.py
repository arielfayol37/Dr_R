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
    class DifficultyChoices(models.TextChoices):
        EASY = 'EASY', 'Easy'
        MEDIUM = 'MEDIUM', 'Medium'
        DIFFICULT = 'DIFFICULT', 'Difficult'

    class SubjectChoices(models.TextChoices):    

        COMPUTER_SCIENCE = 'COMPUTER_SCIENCE', 'Computer Science'
        MATHS = 'MATHS', 'Maths'
        PHYSICS = 'PHYSICS', 'Physics'
        # TODO: Add more subject choices as needed.

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
    # TODO: Predefine common topics and implement the select field in the `create_course` template such that the instructor
            may add a new topic if it doesn't already exist.
            MECHANICS = 'Mechanics'
            THERMODYNAMICS = 'Thermodynamics'
            ELECTRICITY_MAGNETISM = 'Electricity and Magnetism'
            WAVES_OPTICS = 'Waves and Optics'
            MODERN_PHYSICS = 'Modern Physics'
            FLUID_MECHANICS = 'Fluid Mechanics'
            OSCILLATIONS_WAVES = 'Oscillations and Waves'
            OPTICS_LIGHT = 'Optics and Light'

            TOPIC_CHOICES = [
                (MECHANICS, 'Mechanics'),
                (THERMODYNAMICS, 'Thermodynamics'),
                (ELECTRICITY_MAGNETISM, 'Electricity and Magnetism'),
                (WAVES_OPTICS, 'Waves and Optics'),
                (MODERN_PHYSICS, 'Modern Physics'),
                (FLUID_MECHANICS, 'Fluid Mechanics'),
                (OSCILLATIONS_WAVES, 'Oscillations and Waves'),
                (OPTICS_LIGHT, 'Optics and Light'),
]
    # TODO: A question will most likely be part of an `Assignment` which will be part of a `Course`
            As such, it will be very redudant for the instructor to specify the topic each time, because
            the topic will likely be correlated to the `Course`. For example, Ampere's Law will be a sub topic
            of `ELECTRICITY_MAGNETISM` topic which will likely be the main topic of the course Electromagnetism.
            So we want the professor to specify the subtopic, not the topic most of the time. In that regard,
            the topic should by default have the same name or similar to that of the course, and the instructor
            may choose another topic name from the dropdown list. 
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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

 

    text = models.TextField(null=False, blank=False)
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE, \
                                   related_name="questions")
    category = models.CharField(max_length=50, null=True, blank=True)
    # TODO: The topic will most likely be the same as that as one of the topics of the `Course`
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    # TODO: The sub_topic is what we want the instructor to enter
    sub_topic = models.CharField(max_length=50, null=True, blank=True)
    num_points = models.IntegerField(default=10) # Add lower and upper bound.
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, \
                                        blank=True, related_name='sub_questions')
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
    # TODO: (maybe) Change related name to 'answers'.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="float_answers")
    content = models.FloatField(blank=False, null=False)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
            
        return f"Float Answer for {self.question}: {self.content}"
        
            

class ExpressionAnswer(models.Model):
    """
    An expression for a structural question may just be interpreted as text. The math.js library
    will parse the expression given by the teacher and the resulting text will be stored.
    When a user will input an answer, it will be compared to that text.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="expression_answers")
    content = models.CharField(max_length=100) 
    

    def __str__(self):
        
        return f"Expression Answer for {self.question}: {self.content}"

    

class VectorAnswer(models.Model):
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
