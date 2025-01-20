from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Subject, Course, Exam, Student, Teacher, Video
from django.utils import timezone
class SubjectModelTest(TestCase):
    def test_subject_creation(self):
        subject = Subject.objects.create(name="Mathematics", description="Study of numbers")
        self.assertEqual(subject.name, "Mathematics")
        self.assertEqual(subject.description, "Study of numbers")
        self.assertIsInstance(subject, Subject)

class CourseModelTest(TestCase):
    def test_course_creation(self):
        subject = Subject.objects.create(name="Science", description="Natural Science")
        course = Course.objects.create(
            subject=subject,
            title="Biology 101",
            description="Introduction to Biology",
            start_date="2025-01-01",
            end_date="2025-06-01",
            is_active=True
        )
        self.assertEqual(course.subject, subject)
        self.assertEqual(course.title, "Biology 101")
        self.assertTrue(course.is_active)

class ExamModelTest(TestCase):
    def test_exam_creation(self):
        subject = Subject.objects.create(name="Physics", description="Study of matter")
        teacher_user = User.objects.create_user(username="teacher1", password="password")
        teacher = Teacher.objects.create(user=teacher_user)
        
        # إنشاء تاريخ مع وعي بالمنطقة الزمنية
        exam_date = timezone.make_aware(timezone.datetime(2025, 2, 20, 10, 0, 0))
        
        exam = Exam.objects.create(
            teacher=teacher,
            subject=subject,
            title="Midterm Exam",
            date=exam_date,
            duration=120,
            total_marks=100
        )
        self.assertEqual(exam.teacher, teacher)
        self.assertEqual(exam.subject, subject)
        self.assertEqual(exam.title, "Midterm Exam")

class StudentModelTest(TestCase):
    def test_student_creation_and_courses(self):
        student_user = User.objects.create_user(username="student1", password="password")
        student = Student.objects.create(user=student_user, student_year="Year 1", student_id=1001)
        subject = Subject.objects.create(name="Math", description="Study of numbers")
        course = Course.objects.create(
            subject=subject,
            title="Algebra 101",
            description="Introduction to Algebra",
            start_date="2025-01-10",
            end_date="2025-06-15",
            is_active=True
        )
        student.courses.add(course)
        self.assertEqual(student.courses.count(), 1)
        self.assertEqual(student.courses.first().title, "Algebra 101")

class TeacherModelTest(TestCase):
    def test_teacher_creation_and_subjects(self):
        teacher_user = User.objects.create_user(username="teacher1", password="password")
        teacher = Teacher.objects.create(user=teacher_user, specialty="Physics")
        subject = Subject.objects.create(name="Physics", description="Study of matter")
        teacher.subjects.add(subject)
        self.assertEqual(teacher.subjects.count(), 1)
        self.assertEqual(teacher.subjects.first().name, "Physics")

class VideoModelTest(TestCase):
    def test_video_creation(self):
        subject = Subject.objects.create(name="Computer Science", description="Study of computers")
        course = Course.objects.create(
            subject=subject,
            title="Programming 101",
            description="Introduction to Programming",
            start_date="2025-01-15",
            end_date="2025-06-15",
            is_active=True
        )
        teacher_user = User.objects.create_user(username="teacher2", password="password")
        teacher = Teacher.objects.create(user=teacher_user)
        video = Video.objects.create(
            course=course,
            teacher=teacher,
            title="Lecture 1",
            url="https://example.com/lecture1",
            description="Introduction to Programming"
        )
        self.assertEqual(video.course, course)
        self.assertEqual(video.teacher, teacher)
        self.assertEqual(video.title, "Lecture 1")
