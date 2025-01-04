from rest_framework import serializers  
from .models import Subject, Course, Student, Teacher, Exam, Video  

class SubjectSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Subject  
        fields = ['id', 'name', 'description']  


class CourseSerializer(serializers.ModelSerializer):  
    subject = SubjectSerializer()   

    class Meta:  
        model = Course  
        fields = ['id', 'subject', 'title', 'description', 'start_date', 'end_date']  


class StudentSerializer(serializers.ModelSerializer):  
    courses = CourseSerializer(many=True)  
    subject = SubjectSerializer()  

    class Meta:  
        model = Student  
        fields = ['id', 'user', 'courses', 'subject']  


class TeacherSerializer(serializers.ModelSerializer):  
    subject = SubjectSerializer()  

    class Meta:  
        model = Teacher  
        fields = ['id', 'user', 'subject']  


class ExamSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Exam  
        fields = ['id', 'title', 'date', 'duration', 'total_marks']  


class VideoSerializer(serializers.ModelSerializer):  
    course = CourseSerializer()  
    teacher = TeacherSerializer()  

    class Meta:  
        model = Video  
        fields = ['id', 'course', 'teacher', 'title', 'url', 'description']