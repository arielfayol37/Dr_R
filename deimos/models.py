from django.db import models
from phobos.models import Course, Question, User

class Student(User):
    """
    Student class to handle students in the platform.
    
    # TODO: Can add profile pictures if deemed fit. 
    # TODO: May add school name if platform scales.
    """
    courses = models.ManyToManyField(Course, through='Enrollment')
    notes = models.ManyToManyField(Question, through='Note')

class Note(models.Model):
    """
    For any particular question, the Student should have the option to 
    write text and/orupload pictures for their own personal use whenever 
    they are viewing the question in the future. 
    This may be helpful when they are preparing for exams.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    note_text = models.TextField()

class NoteImage(models.Model):
    """
    Stored in Student's Note in case the student upload pictures for notes on a
    particular question.
    """
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='deimos/images/note_images/', blank=True, null=True)
 

class Resource(models.Model):
    """
    Used to store resources suggested by Student.

    For example, if the Student has a web page that he/she deemed
    helpful for a particular question, he/she may submit it.

    This will be later validated by the Professor, and can be
    suggested to other students automatically.
    
    If there are many suggested Resources for the question, 
    an algorithm will take care of the order of recommendation, based
    on other students ratings of the Resource, and/or the student answering
    the question particular needs.
    """
    url = models.URLField(blank=False, null=False) # User must input URL
    description = models.TextField(blank = False) # User must provide description
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

class BonusPoint(models.Model):
    """
    These are bonus points gained by the Student, upon approval of suggested
    resources. 

    These bonus points may be used in two ways:
        1) Direct increase in the Student's grade
        2) To give more attempts(with no deductions per attempt) to the Student
           for any question they would like.
           For example, there maybe a button at the top of the page to click,
           which will 'detect' the question the user is on, and give more attempts
           (page maybe reloaded with updated info-new attempts- or 
           that can be handled dynamically using fetch() in JS, while updating the display
           for a better experience)

    """
    points = models.IntegerField()
    resource = models.OneToOneField(Resource, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Enrollment(models.Model):
    """
    Used to handle a student's enrollment for a particular course.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField()
