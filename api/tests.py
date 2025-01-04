from django.test import TestCase  
from .models import Subject, Course, Student, Teacher, Exam, Video  
from django.contrib.auth.models import User  

class SubjectModelTest(TestCase):  
    def setUp(self):  
        self.subject = Subject.objects.create(name='Mathematics', description='Study of numbers')  

    def test_subject_creation(self):  
        self.assertEqual(self.subject.name, 'Mathematics')  
        self.assertEqual(self.subject.description, 'Study of numbers')  

class CourseModelTest(TestCase):  
    def setUp(self):  
        self.subject = Subject.objects.create(name='Mathematics')  
        self.course = Course.objects.create(  
            subject=self.subject,  
            title='Algebra',  
            description='Algebra course',  
            start_date='2025-01-01',  
            end_date='2025-06-01'  
        )  

    def test_course_creation(self):  
        self.assertEqual(self.course.title, 'Algebra')  
        self.assertEqual(self.course.subject.name, 'Mathematics')  

class StudentModelTest(TestCase):  
    def setUp(self):  
        self.user = User.objects.create_user(username='student1', password='testpass')  
        self.subject = Subject.objects.create(name='Mathematics')  
        self.course = Course.objects.create(  
            subject=self.subject,  
            title='Algebra',  
            start_date='2025-01-01',  
            end_date='2025-06-01'  
        )  
        self.student = Student.objects.create(user=self.user, subject=self.subject)  
        self.student.courses.add(self.course)  

    def test_student_creation(self):  
        self.assertEqual(self.student.user.username, 'student1')  
        self.assertIn(self.course, self.student.courses.all())  

class TeacherModelTest(TestCase):  
    def setUp(self):  
        self.user = User.objects.create_user(username='teacher1', password='testpass')  
        self.subject = Subject.objects.create(name='Mathematics')  
        self.teacher = Teacher.objects.create(user=self.user, subject=self.subject)  

    def test_teacher_creation(self):  
        self.assertEqual(self.teacher.user.username, 'teacher1')  
        self.assertEqual(self.teacher.subject.name, 'Mathematics')  

class ExamModelTest(TestCase):  
    def setUp(self):  
        self.exam = Exam.objects.create(title='Midterm Exam', date='2025-03-01T10:00:00Z', duration=120, total_marks=100)  

    def test_exam_creation(self):  
        self.assertEqual(self.exam.title, 'Midterm Exam')  
        self.assertEqual(self.exam.total_marks, 100)  

class VideoModelTest(TestCase):  
    def setUp(self):  
        self.user = User.objects.create_user(username='teacher1', password='testpass')  
        self.subject = Subject.objects.create(name='Mathematics')  
        self.course = Course.objects.create(subject=self.subject, title='Algebra', start_date='2025-01-01', end_date='2025-06-01')  
        self.teacher = Teacher.objects.create(user=self.user, subject=self.subject)  
        self.video = Video.objects.create(course=self.course, teacher=self.teacher, title='Introduction to Algebra', url='http://example.com/video', description='A video about algebra.')  

    def test_video_creation(self):  
        self.assertEqual(self.video.title, 'Introduction to Algebra')  
        self.assertEqual(self.video.course.title, 'Algebra')