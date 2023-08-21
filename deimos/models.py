from django.db import models
from phobos.models import Course, Question, User, Assignment, VariableInstance, QuestionChoices
from django.core.validators import MaxValueValidator, MinValueValidator
class Student(User):
    """
    Student class to handle students in the platform.
    
    # TODO: Can add profile pictures if deemed fit. 
    # TODO: May add school name if platform scales.
    """
    courses = models.ManyToManyField(Course, through='Enrollment')
    assignments = models.ManyToManyField(Assignment, through='AssignmentStudent')
    questions = models.ManyToManyField(Question, through='QuestionStudent')

class Note(models.Model):
    """
    For any particular question, the Student should have the option to 
    write text and/orupload pictures for their own personal use whenever 
    they are viewing the question in the future. 
    This may be helpful when they are preparing for exams.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="notes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()

class NoteImage(models.Model):
    """
    Stored in `Student`'s Note in case the student upload pictures for notes on a
    particular question.
    """
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='deimos/images/notes_images/', blank=True, null=True)
 

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='resources')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False, null=True)

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
    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, related_name='bonuses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Enrollment(models.Model):
    """
    Used to handle a `Student`'s enrollment for a particular course.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(validators=[MaxValueValidator(100)], default=0, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

class AssignmentStudent(models.Model):
    """
    Used to manage `Assigment` - `Student` relationship.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments_intermediate')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.FloatField(validators=[MaxValueValidator(100)], default=0, null=True)

    def get_grade(self):
        """
        Computes and returns the grade of a student on an Assignment
        """
        num_points = 0
        total = 0
        for question in self.assignment.questions:
            question_student = QuestionStudent.objects.filter(\
                question=question, student=self.student)
            total += question.num_points
            num_points += question_student.get_num_points()
        self.grade = (num_points/total) * 100
        return self.grade
class QuestionStudent(models.Model):
    """
    Used to manage `Question` - `Student` relationship.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    num_points = models.FloatField(default=0)
    success = models.BooleanField(default=False)
    var_instances = models.ManyToManyField(VariableInstance, related_name='question_students')
    instances_created = models.BooleanField(default=False)
    def create_instances(self):
        """
        Get variable instances from the variables associated to the question.
        """
        self.var_instances.clear()
        for var in self.question.variables.all():
            self.var_instances.add(var.get_instance())
        self.instances_created = True
    def compute_structural_answer(self):
        """
        Computes the answer to the question if it's a `Question` with `Variable` answers.
        """
        if not self.instances_created:
            self.create_instances()
        if self.question.answer_type == QuestionChoices.STRUCTURAL_VARIABLE_FLOAT:
            assert self.question.variable_float_answers.count() == 1
            answer = self.question.variable_float_answers.first().content
            for var_instance in self.var_instances:
                answer = answer.replace(var_instance.variable.symbol, var_instance.value)
        # TODO: Add a clause here if the answer type is different
        # TODO: Add another clause here to make sure the answer evaluates to a float.
            return eval(answer)
    def get_var_value_dict(self):
        """
        Returns a dictionary of variable symbols and the corresponding instance value for
        this particular `Question`-`Student`.
        """
        var_value_dict = {}
        for var_instance in self.var_instances:
            var_value_dict[var_instance.variable.symbol] = var_instance.value
        return var_value_dict
    def compute_mcq_answers(self):
        """
        Computes the float anwers to an MCQ question if they were variables.
        """
        if self.question.answer_type.startswith('MCQ'):
            mcq_var_floats = self.question.mcq_variable_float_answers.all()
            answers = []
            for mcq_var_float in mcq_var_floats:
                answer = mcq_var_float.content
                for var_instance in self.var_instances:
                    answer = answer.replace(var_instance.variable.symbol, var_instance.value)
                answers.append(eval(answer))
            return answers
        
    def get_num_points(self):
        """
        Calculates and returns the number of points a student gets from a question
        """
        total = 0
        for attempt in self.attempts:
            # The idea here is that at some point
            # the student may get points even if attempts
            # are not successful. Maybe due to a new functionality
            # or the teacher manually giving points for that attempt
            total += attempt.num_points
        self.num_points = total
        return total 
    
    def get_num_attempts(self):
        """
        Calculates and returns the number of attempts on a question by a user.
        """
        return self.attempts.count()
    def __str__(self):
        return f"Question-Student:{self.question} {self.student.username}"
    
    
class QuestionAttempt(models.Model):
    """
    Used to manage `Student` attempts on `Question`s
    """
    content = models.CharField(max_length=1000, blank=False, null=False)
    question_student = models.ForeignKey(QuestionStudent, on_delete=models.CASCADE, related_name='attempts')
    success = models.BooleanField(default=False, null=True)
    num_points = models.FloatField(default=0, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_student.student.username} attempt for {self.question_student.question}"