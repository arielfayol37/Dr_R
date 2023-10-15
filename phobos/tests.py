from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Professor, Topic, SubTopic, Assignment, Question, Subject

class ModelTests(TestCase):

    def setUp(self):
        self.professor = Professor.objects.create(username='professor1',\
                                                  email='prof@valpo.edu',\
                                                     first_name='Jim',
                                                      last_name='Carter', department='Computer Science')
        self.subject = Subject.objects.get(name='PHYSICS')
        self.topic = Topic.objects.create(name='Topic 1', subject=self.subject)
        self.course = Course.objects.create(name='Course 1', subject='COMPUTER_SCIENCE', number_of_students=50)
        self.course.professors.add(self.professor)
        self.course.topics.add(self.topic)
        self.assignment = Assignment.objects.create(name='Assignment 1', course=self.course)

    def test_course_creation(self):
        """ 
        Checking whether course attributes were assigned properly.
        """
        self.assertTrue(self.course.professors.filter(pk=self.professor.pk).exists())
        self.assertEqual(self.course.name, 'Course 1')
        self.assertEqual(self.course.subject, 'COMPUTER_SCIENCE')
        self.assertEqual(self.course.number_of_students, 50)

    def test_assignment_creation(self):
        """ Testing assignment was properly created. """
        self.assertEqual(self.assignment.name, 'Assignment 1')
        self.assertEqual(self.assignment.course, self.course)

    def test_question_creation(self):
        """ Testing question was properly created """
        question = Question.objects.create(number='Q1', text='Sample question', assignment=self.assignment)
        self.assertEqual(question.number, 'Q1')
        self.assertEqual(question.text, 'Sample question')
        self.assertEqual(question.assignment, self.assignment)

    def test_professor_creation(self):
        """ Testing professor's department. """
        self.assertEqual(self.professor.department, 'Computer Science')

    def test_topic_creation(self):
        """ Testing topic was properly created. """
        self.assertEqual(self.topic.name, 'Topic 1')

    def test_subtopic_creation(self):
        """ Testing subtopic was properly created. """
        subtopic = SubTopic.objects.create(topic=self.topic, name='Subtopic 1')
        self.assertEqual(subtopic.topic, self.topic)
        self.assertEqual(subtopic.name, 'Subtopic 1')


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.professor = Professor.objects.create(username='professor1',\
                                                  email='prof@email.com',\
                                                     first_name='Jim',
                                                      last_name='Carter', department='Computer Science',
                                                      password='testpassword')

        self.subject = Subject.objects.get(name='PHYSICS')
        self.topic = Topic.objects.create(name='Topic 1', subject=self.subject)
        self.course = Course.objects.create(name='Course 1', subject='COMPUTER_SCIENCE')
        self.course_2 = Course.objects.create(name='Course 2', subject='PHYSICS')
        self.course.professors.add(self.professor)
        self.course_2.professors.add(self.professor)
        self.course.topics.add(self.topic)

        self.assignment = Assignment.objects.create(name='Assignment 1', course=self.course)
        self.question = Question.objects.create(number='Q1', text='Sample question', assignment=self.assignment)


    def test_create_course_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('phobos:create_course'), {'name': 'New Course'})
        self.assertEqual(response.status_code, 302)  # Or 302 for a successful redirect
        # Add assertions for the newly created course

    def test_create_assignment_view(self):
        """ Testing assignment creation. """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('phobos:create_assignment'), {'name': 'New Assignment'})
        self.assertEqual(response.status_code, 302)  # Or 302 for a successful redirect
        

    def test_create_question_view(self):
        """ Testing question creation. """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('phobos:create_question', args=[self.assignment.id]), {'question_text': 'New Question'})
        self.assertEqual(response.status_code, 302)  # Or 302 for a successful redirect
"""
TODO: fix the following tests.
    def test_login_view(self):
        #Testing login view.
        response = self.client.post(reverse('phobos:index'), {'email': 'prof@email.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        #Testing professor login and index page.
        response = self.client.post(reverse('phobos:login'), {
            'email': 'prof@email.com',
            'password': 'testpassword',
        })
        self.assertTrue(response, "Login was not successful")  # Check if login was successful
        logged = self.client.login(username='professor1', password='testpassword', email='prof@email.com')
        print(f'logged in: {logged}')
        response = self.client.get('/phobos/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('courses', response.context) 
        self.assertEqual(response.context['courses'].count(), 2)

"""


