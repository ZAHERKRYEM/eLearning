from rest_framework import viewsets  
from .models import Subject, Course, Student, Teacher, Exam, Video  
from .serializers import (  
    SubjectSerializer,  
    CourseSerializer,  
    StudentSerializer,  
    TeacherSerializer,  
    ExamSerializer,  
    VideoSerializer  
)  

class SubjectViewSet(viewsets.ModelViewSet):  
    queryset = Subject.objects.all()  
    serializer_class = SubjectSerializer  


class CourseViewSet(viewsets.ModelViewSet):  
    queryset = Course.objects.all()  
    serializer_class = CourseSerializer  


class StudentViewSet(viewsets.ModelViewSet):  
    queryset = Student.objects.all()  
    serializer_class = StudentSerializer  


class TeacherViewSet(viewsets.ModelViewSet):  
    queryset = Teacher.objects.all()  
    serializer_class = TeacherSerializer  


class ExamViewSet(viewsets.ModelViewSet):  
    queryset = Exam.objects.all()  
    serializer_class = ExamSerializer  


class VideoViewSet(viewsets.ModelViewSet):  
    queryset = Video.objects.all()  
    serializer_class = VideoSerializer